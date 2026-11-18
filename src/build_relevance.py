"""
Build data/processed/comments_relevance_v1.csv: corpus-level relevance (relevant = y / n).

Rule (see CLAUDE.md, "Pass 1 labels and outlier reduction"):
  route == relevant       -> y   (topic labelled relevant; source = topic label (<label source>))
  route == excluded       -> n   (topic labelled not_relevant, or outlier left at -1)
  route == check_comment  -> comment-level label from labelling/relevansi_check_comment_final.csv
                             (human label on the 100 validation comments, Claude v2 otherwise)

Inputs:  experiments/pass1_v1_nn15_mcs15_a/doc_topics_reduced.csv
         experiments/pass1_v1_nn15_mcs15_a/labelling/relevansi_check_comment_final.csv
Usage:   python src/build_relevance.py [--check]   (--check compares with the existing file, writes nothing)
"""

import argparse
from pathlib import Path

import pandas as pd

RUN = Path("experiments/pass1_v1_nn15_mcs15_a")
OUT = Path("data/processed/comments_relevance_v1.csv")
COLS = ["commentId", "videoId", "case_id", "org_type", "video_type", "verification_status", "isReply",
        "likeCount", "topic", "assigned_by", "route", "relevant", "relevance_source", "textOriginal", "text_embed"]


def build():
    d = pd.read_csv(RUN / "doc_topics_reduced.csv", encoding="utf-8-sig", dtype={"commentId": str})
    c = pd.read_csv(RUN / "labelling" / "relevansi_check_comment_final.csv", encoding="utf-8-sig",
                    dtype={"commentId": str}).set_index("commentId")
    d["relevant"] = d.route.map({"relevant": "y", "excluded": "n"})
    d["relevance_source"] = "topic label (" + d.label_source.fillna("outlier -1") + ")"
    chk = d.route == "check_comment"
    missing = set(d.loc[chk, "commentId"]) - set(c.index)
    assert not missing, f"{len(missing)} check_comment rows without a comment-level label"
    d.loc[chk, "relevant"] = d.loc[chk, "commentId"].map(c.relevant_final)
    d.loc[chk, "relevance_source"] = d.loc[chk, "commentId"].map(c.relevance_source)
    assert d.relevant.isin(["y", "n"]).all()
    return d[COLS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()
    d = build()
    if a.check:
        old = pd.read_csv(OUT, encoding="utf-8-sig", dtype={"commentId": str})
        same = (old.commentId.equals(d.commentId) and old.relevant.equals(d.relevant))
        src = (old.relevance_source == d.relevance_source).mean()
        print(f"rows {len(d)}, relevant y {int((d.relevant == 'y').sum())}; "
              f"identical ids+labels: {same}; relevance_source match {src:.1%}")
        return
    if OUT.exists() and not a.overwrite:
        raise SystemExit(f"{OUT} exists; use --check or --overwrite")
    d.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"wrote {OUT}: {len(d)} rows, {int((d.relevant == 'y').sum())} relevant")


if __name__ == "__main__":
    main()
