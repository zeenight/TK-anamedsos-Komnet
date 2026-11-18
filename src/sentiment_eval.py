"""
Evaluate the two pretrained sentiment models against human stance labels (TK3 criterion 4).

The models have no extra labelled training data, so TK3 asks for an evaluation of their
limits. Gold standard: the 100-comment blind validation sample of the stance step after
adjudication (experiments/stance_v1/validasi_sikap_final.csv, column sikap_final).
Zillan's blind labels are reported as a second reference.

Two readings, both stated explicitly because sentiment (tone) and stance are not the same construct:
  1. binary: "negative" sentiment used as a detector of objection (sikap = tolak);
  2. 3-class mapping: negative -> tolak, neutral -> lain, positive -> dukung.
Also a descriptive cross-tab of sentiment vs stance on all 2,288 relevant comments
(stance there = sikap_final_v2, mostly Claude labels, not a gold standard).

Output: experiments/sentiment_eval_v1/ (sentiment_eval.json, tabel_sentimen_eval.md,
crosstab_sentimen_sikap.csv, fig8_confusion_sentimen.png)

Usage (from the project root):  python src/sentiment_eval.py
"""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report, cohen_kappa_score,
                             confusion_matrix, precision_recall_fscore_support)

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

VERSION = "1.0"
OUT = Path("experiments/sentiment_eval_v1")
MODELS = {"id": "w11wo/indonesian-roberta-base-sentiment-classifier",
          "xlmr": "cardiffnlp/twitter-xlm-roberta-base-sentiment"}
MAP3 = {"negative": "tolak", "neutral": "lain", "positive": "dukung"}
CLS = ["tolak", "lain", "dukung"]
SENT = ["negative", "neutral", "positive"]
INK, INK2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
SEQ = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def evaluate(gold, sent):
    pred3 = sent.map(MAP3)
    yb, pb = (gold == "tolak").astype(int), (sent == "negative").astype(int)
    p, r, f, _ = precision_recall_fscore_support(yb, pb, average="binary", zero_division=0)
    rep = classification_report(gold, pred3, labels=CLS, output_dict=True, zero_division=0)
    return {
        "n": int(len(gold)),
        "biner_negatif_vs_tolak": {"accuracy": round(accuracy_score(yb, pb), 3),
                                   "precision": round(p, 3), "recall": round(r, 3), "f1": round(f, 3)},
        "tiga_kelas": {"accuracy": round(accuracy_score(gold, pred3), 3),
                       "macro_f1": round(rep["macro avg"]["f1-score"], 3),
                       "kappa": round(cohen_kappa_score(gold, pred3, labels=CLS), 3),
                       "per_kelas": {c: {k: round(rep[c][k], 3) for k in ["precision", "recall", "f1-score"]}
                                     | {"support": int(rep[c]["support"])} for c in CLS}},
        "confusion_matrix": {"baris_label_manusia": CLS, "kolom_sentimen": SENT,
                             "nilai": confusion_matrix(gold, pred3, labels=CLS).tolist()},
    }


def fig(cms, n):
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.9), facecolor=SURFACE)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("seq", SEQ)
    vmax = max(np.max(c) for c in cms.values())
    for ax, (m, cm) in zip(axes, cms.items()):
        cm = np.array(cm)
        ax.imshow(cm, cmap=cmap, vmin=0, vmax=vmax)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=11,
                        color="white" if cm[i, j] > vmax * 0.55 else INK)
        ax.set_xticks(range(3))
        ax.set_xticklabels(["negatif", "netral", "positif"], fontsize=9, color=INK2)
        ax.set_yticks(range(3))
        ax.set_yticklabels(CLS, fontsize=9, color=INK2)
        ax.set_xlabel("Prediksi sentimen", fontsize=9, color=INK2)
        if m == "id":
            ax.set_ylabel("Sikap (label manusia)", fontsize=9, color=INK2)
        ax.set_title({"id": "IndoRoBERTa (id)", "xlmr": "XLM-R Twitter (xlmr)"}[m],
                     loc="left", fontsize=10, color=INK)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
    fig.suptitle("Sentimen pretrained vs sikap manusia", x=0.02, ha="left", fontsize=11, color=INK)
    fig.text(0.01, 0.01, f"Sampel validasi sikap setelah adjudikasi (n={n}). Diagonal = cocok "
             "(negatif-tolak, netral-lain, positif-dukung).", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(OUT / "fig8_confusion_sentimen.png", dpi=300)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sen = pd.read_csv("data/processed/comments_sentiment_v1.csv",
                      usecols=["commentId", "case_id", "sent_id", "sent_xlmr"])
    val = pd.read_csv("experiments/stance_v1/validasi_sikap_final.csv")
    v = val.merge(sen, on="commentId", how="left")
    assert v.sent_id.notna().all(), "validation comment without sentiment"

    res = {"script": f"src/sentiment_eval.py v{VERSION}", "model": MODELS,
           "gold": "experiments/stance_v1/validasi_sikap_final.csv (sikap_final, setelah adjudikasi)"}
    cms = {}
    for m in MODELS:
        res[f"{m}_vs_final"] = evaluate(v.sikap_final, v[f"sent_{m}"])
        b = v[v.sikap_zillan_blind.notna()]
        res[f"{m}_vs_zillan_blind"] = evaluate(b.sikap_zillan_blind, b[f"sent_{m}"])
        cms[m] = res[f"{m}_vs_final"]["confusion_matrix"]["nilai"]
    # baseline: always predict the majority class (tolak)
    res["baseline_mayoritas_tolak"] = {"accuracy": round((v.sikap_final == "tolak").mean(), 3)}

    # descriptive cross-tab on all relevant comments (not a gold standard)
    sik = pd.read_csv("experiments/stance_v1/sikap_final_v2.csv", usecols=["commentId", "sikap"])
    a = sik.merge(sen, on="commentId")
    ct = []
    for m in MODELS:
        t = pd.crosstab(a.sikap, a[f"sent_{m}"]).reindex(index=CLS, columns=SENT, fill_value=0)
        t.insert(0, "model", m)
        ct.append(t.reset_index())
    ct = pd.concat(ct)
    ct.to_csv(OUT / "crosstab_sentimen_sikap.csv", index=False)
    res["crosstab_semua_relevan_n"] = int(len(a))

    (OUT / "sentiment_eval.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    fig(cms, len(v))

    rows = []
    for m in MODELS:
        for ref in ["final", "zillan_blind"]:
            r = res[f"{m}_vs_{ref}"]
            b, t = r["biner_negatif_vs_tolak"], r["tiga_kelas"]
            rows.append(f"| {m} | {ref} | {r['n']} | {b['precision']} | {b['recall']} | {b['f1']} | "
                        f"{t['accuracy']} | {t['macro_f1']} | {t['kappa']} | "
                        + " | ".join(str(t["per_kelas"][c]["f1-score"]) for c in CLS) + " |")
    md = ["# Evaluasi sentimen pretrained terhadap label sikap manusia", "",
          f"Dibuat oleh `src/sentiment_eval.py` v{VERSION}. Baseline selalu-tolak: akurasi "
          f"{res['baseline_mayoritas_tolak']['accuracy']}.", "",
          "| model | acuan | n | P (neg→tolak) | R | F1 | akurasi 3 kelas | macro-F1 | κ | F1 tolak | F1 lain | F1 dukung |",
          "|" + "---|" * 12, *rows, "",
          "## Tabulasi silang sentimen × sikap (2.288 komentar relevan; sikap = sikap_final_v2)", "",
          "| model | sikap | negative | neutral | positive |", "|---|---|---|---|---|",
          *[f"| {r.model} | {r.sikap} | {r.negative} | {r.neutral} | {r.positive} |" for r in ct.itertuples()], ""]
    (OUT / "tabel_sentimen_eval.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Output in {OUT}")


if __name__ == "__main__":
    main()
