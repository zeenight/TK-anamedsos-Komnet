"""Automated label check without Cohen's kappa (v1.0).

A logistic-regression classifier on the cached mpnet embeddings learns
Claude's labels (sikap, tema_utama) from the comments outside the human
validation sample. Two automated checks:

1. Consistency: grouped cross-validation (split by authorHash, then
   leave-one-case-out). If the labels follow consistent rules, a simple
   model can learn them; macro-F1 per class shows which labels are fuzzy.
2. Independent comparison: on the 100 validation comments the model,
   which never saw them, is compared with the human *blind* labels,
   next to Claude's own pre-adjudication labels.

Metrics: accuracy and macro-F1 (no kappa). Run from the project root:
    python experiments/auto_check_v1/auto_check.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import LeaveOneGroupOut, StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

OUT = Path("experiments/auto_check_v1")
SEED = 42

emb = np.load("data/processed/embeddings_mpnet_v1.npy")
corpus = pd.read_csv("data/processed/comments_bertopic_v1.csv", usecols=["commentId", "authorHash", "case_id"])
assert len(corpus) == emb.shape[0]
row_of = {cid: i for i, cid in enumerate(corpus["commentId"])}


def model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.05, class_weight="balanced", max_iter=3000))


def scores(y_true, y_pred, labels):
    return {
        "n": int(len(y_true)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 3),
        "macro_f1": round(float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)), 3),
        "f1_per_class": {k: round(v["f1-score"], 3) for k, v in classification_report(
            y_true, y_pred, labels=labels, output_dict=True, zero_division=0).items() if k in labels},
    }


def run(task, df, label_col, sample_ids, blind, claude_v1):
    df = df[df["commentId"].isin(row_of)].copy()
    df["row"] = df["commentId"].map(row_of)
    df["authorHash"] = corpus["authorHash"].values[df["row"]]
    train = df[~df["commentId"].isin(sample_ids)]
    labels = sorted(train[label_col].unique())
    X, y = emb[train["row"]], train[label_col].values
    res = {"task": task, "labels": labels, "n_train": int(len(train)),
           "label_dist_train": train[label_col].value_counts().to_dict()}

    # 1. consistency of Claude's labels
    pred = np.empty(len(y), dtype=object)
    for tr, te in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(X, y, train["authorHash"]):
        pred[te] = model().fit(X[tr], y[tr]).predict(X[te])
    res["cv_author"] = scores(y, pred, labels)
    pred = np.empty(len(y), dtype=object)
    for tr, te in LeaveOneGroupOut().split(X, y, train["case_id"]):
        pred[te] = model().fit(X[tr], y[tr]).predict(X[te])
    res["cv_leave_case_out"] = scores(y, pred, labels)
    res["cv_leave_case_out"]["accuracy_per_case"] = {
        c: round(float((pred[m] == y[m]).mean()), 3) for c in sorted(train["case_id"].unique())
        for m in [(train["case_id"] == c).values]}

    # 2. sample of 100: model (never saw it) vs human blind, Claude v1 vs human blind
    s = pd.DataFrame({"commentId": list(blind)}).assign(blind=lambda d: d["commentId"].map(blind),
                                                       claude=lambda d: d["commentId"].map(claude_v1))
    s = s[s["blind"].isin(labels) & s["commentId"].isin(row_of)]
    s["model"] = model().fit(X, y).predict(emb[s["commentId"].map(row_of)])
    res["sample_model_vs_human_blind"] = scores(s["blind"], s["model"], labels)
    res["sample_claude_vs_human_blind"] = scores(s["blind"], s["claude"], labels)
    res["sample_model_vs_claude"] = scores(s["claude"], s["model"], labels)
    s.to_csv(OUT / f"sampel_{task}.csv", index=False)
    return res


sik = pd.read_csv("experiments/stance_v1/sikap_final_v2.csv")
vs = pd.read_csv("experiments/stance_v1/validasi_sikap_final.csv")
r_sikap = run("sikap", sik, "sikap_claude_v2", set(vs["commentId"]),
              dict(zip(vs["commentId"], vs["sikap_zillan_blind"])), dict(zip(vs["commentId"], vs["sikap_claude"])))

tem = pd.read_csv("experiments/themes_v1/tema_final_v2.csv")
tem = tem[tem["tema_utama"] != "LT"]
vt = pd.read_csv("experiments/themes_v1/validasi_tema_final.csv")
r_tema = run("tema", tem, "tema_utama", set(vt["commentId"]),
             dict(zip(vt["commentId"], vt["validator"])), dict(zip(vt["commentId"], vt["claude_v1"])))

out = {"version": "auto_check v1.0", "seed": SEED,
       "model": "StandardScaler + LogisticRegression(C=0.05, class_weight=balanced) on paraphrase-multilingual-mpnet-base-v2 embeddings",
       "sikap": r_sikap, "tema": r_tema}
(OUT / "auto_check_hasil.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
for r in (r_sikap, r_tema):
    print(f"\n== {r['task']} (n_train {r['n_train']})")
    for k in ("cv_author", "cv_leave_case_out", "sample_model_vs_human_blind", "sample_claude_vs_human_blind", "sample_model_vs_claude"):
        print(f"{k:32s} n={r[k]['n']:4d} acc={r[k]['accuracy']:.3f} macroF1={r[k]['macro_f1']:.3f}  {r[k]['f1_per_class']}")
    print("acc per case (leave-case-out):", r["cv_leave_case_out"]["accuracy_per_case"])
