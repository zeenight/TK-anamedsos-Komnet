"""
Descriptive analytics for TK3 (criterion 2): dataset, users, temporal, engagement, content.

Every measure is chosen for its link to the RQs, not to report every statistic:
  - dataset/users per case: how unbalanced the corpus is and how concentrated authorship is
    (comments are not independent observations, see the chi-square note in tabel_final.md);
  - temporal: when comments arrived relative to the video upload, and whether the stance /
    theme mix of early comments differs from later ones (RQ3: re-uploads vs third-party);
  - engagement: whether likes concentrate on certain stances/themes (likes are context only,
    never a weight for theme prevalence);
  - content: distinctive words of objection comments per org type and video type
    (weighted log-odds with an informative Dirichlet prior, Monroe et al. 2008).

Inputs (all existing, nothing is modified):
  data/20260930/comments.csv, data/20260930/videos.csv          raw snapshot
  data/interim/comments_quality_v1.csv                         eligible flag
  data/processed/comments_relevance_v1.csv                     relevant y/n
  data/processed/comments_bertopic_v1.csv                      text_repr_a
  experiments/stance_v1/sikap_final_v2.csv                     stance
  experiments/themes_v1/tema_final_v2.csv                      tema_utama
  resources/stopwords_bertopic_v1.txt

Output: experiments/descriptive_v1/ (tables CSV, ringkasan_deskriptif.json, tabel_deskriptif.md,
fig6_temporal.png, fig7_engagement_tema.png)

Usage (from the project root):  python src/descriptive_stats.py
"""

import json
import re
from collections import Counter
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

VERSION = "1.0"
OUT = Path("experiments/descriptive_v1")
CASES = ["C01", "C02", "C03", "C04", "C05", "C06", "C07"]
THEMES = ["KV", "KO", "PK", "AK", "EJ", "AU", "HC"]
NAMES = {
    "KV": "Kualitas visual", "KO": "Kepantasan organisasi", "PK": "Pekerja kreatif",
    "AK": "Biaya, anggaran & korupsi", "EJ": "Ejekan tanpa alasan", "AU": "Kekhawatiran umum AI",
    "HC": "Hak cipta",
}
VT = {"third_party": "Pihak ketiga", "reupload_archive": "Re-upload/arsip"}
OT = {"government": "Pemerintah", "commercial": "Komersial"}
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def tobool(s):
    return s.astype(str).str.lower().eq("true")


def load():
    raw = pd.read_csv("data/20260930/comments.csv")
    vids = pd.read_csv("data/20260930/videos.csv")
    q = pd.read_csv("data/interim/comments_quality_v1.csv", usecols=["commentId", "eligible"])
    rel = pd.read_csv("data/processed/comments_relevance_v1.csv", usecols=["commentId", "relevant"])
    rep = pd.read_csv("data/processed/comments_bertopic_v1.csv", usecols=["commentId", "text_repr_a"])
    sik = pd.read_csv("experiments/stance_v1/sikap_final_v2.csv", usecols=["commentId", "sikap"])
    tem = pd.read_csv("experiments/themes_v1/tema_final_v2.csv", usecols=["commentId", "tema_utama"])
    df = (raw.merge(q, on="commentId", how="left").merge(rel, on="commentId", how="left")
          .merge(rep, on="commentId", how="left").merge(sik, on="commentId", how="left")
          .merge(tem, on="commentId", how="left"))
    df["eligible"] = tobool(df["eligible"])
    df["isReply"] = tobool(df["isReply"])
    df["isVideoOwner"] = tobool(df["isVideoOwner"])
    df["publishedAt"] = pd.to_datetime(df["publishedAt"], utc=True)
    vids["published_at"] = pd.to_datetime(vids["published_at"], utc=True)
    df = df.merge(vids[["video_id", "published_at", "channel_title", "title"]],
                  left_on="videoId", right_on="video_id", how="left")
    df["days"] = (df["publishedAt"] - df["published_at"]).dt.total_seconds() / 86400
    assert len(df) == len(raw), "merge changed row count"
    return df, vids


def gini(x):
    x = np.sort(np.asarray(x, dtype=float))
    if x.sum() == 0:
        return 0.0
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


def characteristics(df, vids):
    el = df[df.eligible]
    rows = []
    for c in CASES + ["Total"]:
        a = df if c == "Total" else df[df.case_id == c]
        e = el if c == "Total" else el[el.case_id == c]
        v = vids if c == "Total" else vids[vids.case_id == c]
        apc = e.groupby("authorHash").size()
        rows.append({
            "case_id": c,
            "org_type": "" if c == "Total" else a.org_type.iloc[0],
            "video_type": "" if c == "Total" else a.video_type.iloc[0],
            "n_video": len(v),
            "views": int(v.view_count.sum()),
            "komentar_terkumpul": len(a),
            "lolos_kualitas": len(e),
            "relevan": int((e.relevant == "y").sum()),
            "tolak": int((e.sikap == "tolak").sum()),
            "pct_balasan": round(e.isReply.mean() * 100, 1),
            "author_unik": int(e.authorHash.nunique()),
            "komentar_per_author": round(len(e) / e.authorHash.nunique(), 2),
            "pct_author_1_komentar": round((apc == 1).mean() * 100, 1),
            "pct_komentar_dari_author_3plus": round(apc[apc >= 3].sum() / len(e) * 100, 1),
        })
    t = pd.DataFrame(rows)
    # authors active in more than one case
    cases_per_author = el.groupby("authorHash").case_id.nunique()
    apc = el.groupby("authorHash").size()
    users = {
        "author_unik": int(el.authorHash.nunique()),
        "author_lebih_dari_1_kasus": int((cases_per_author > 1).sum()),
        "pct_author_lebih_dari_1_kasus": round((cases_per_author > 1).mean() * 100, 1),
        "max_komentar_satu_author": int(apc.max()),
        "pct_komentar_dari_top1pct_author": round(
            apc.sort_values(ascending=False).head(max(1, int(len(apc) * 0.01))).sum() / len(el) * 100, 1),
        "pct_author_1_komentar": round((apc == 1).mean() * 100, 1),
    }
    return t, users


def temporal(df, vids):
    el = df[df.eligible]
    rows = []
    for _, v in vids.iterrows():
        e = el[el.videoId == v.video_id]
        d = e.days
        rows.append({
            "video_id": v.video_id, "case_id": v.case_id, "video_type": v.video_type,
            "kanal": v.channel_title, "tanggal_unggah": v.published_at.date().isoformat(),
            "komentar_pertama": e.publishedAt.min().date().isoformat(),
            "komentar_terakhir": e.publishedAt.max().date().isoformat(),
            "n": len(e),
            "median_hari_setelah_unggah": round(float(d.median()), 1),
            "pct_dalam_1_hari": round((d <= 1).mean() * 100, 1),
            "pct_dalam_7_hari": round((d <= 7).mean() * 100, 1),
            "pct_dalam_30_hari": round((d <= 30).mean() * 100, 1),
            "pct_setelah_365_hari": round((d > 365).mean() * 100, 1),
        })
    t = pd.DataFrame(rows)

    # stance and theme mix: first 7 days vs later (eligible relevant comments)
    rel = el[el.relevant == "y"].copy()
    rel["periode"] = np.where(rel.days <= 7, "<=7 hari", ">7 hari")
    sik = (pd.crosstab([rel.video_type, rel.periode], rel.sikap, normalize="index") * 100).round(1)
    sik["n"] = pd.crosstab([rel.video_type, rel.periode], rel.sikap).sum(axis=1)
    tol = rel[rel.sikap == "tolak"]
    tem = (pd.crosstab([tol.video_type, tol.periode], tol.tema_utama, normalize="index") * 100).round(1)
    tem = tem[[c for c in THEMES if c in tem.columns]]
    tem["n"] = pd.crosstab([tol.video_type, tol.periode], tol.tema_utama).sum(axis=1)
    return t, sik.reset_index(), tem.reset_index()


def engagement(df):
    el = df[df.eligible]
    rel = el[el.relevant == "y"]

    def summ(g, key):
        rows = []
        tot = g.likeCount.sum()
        for k, s in g.groupby(key):
            rows.append({key: k, "n": len(s), "pct_komentar": round(len(s) / len(g) * 100, 1),
                         "total_like": int(s.likeCount.sum()),
                         "pct_like": round(s.likeCount.sum() / tot * 100, 1),
                         "median_like": float(s.likeCount.median()),
                         "mean_like": round(s.likeCount.mean(), 2),
                         "p90_like": round(float(s.likeCount.quantile(0.9)), 1),
                         "max_like": int(s.likeCount.max()),
                         "pct_like_dari_1_komentar_teratas": round(
                             s.likeCount.max() / max(s.likeCount.sum(), 1) * 100, 1),
                         "pct_nol_like": round((s.likeCount == 0).mean() * 100, 1)})
        return pd.DataFrame(rows)

    by_sikap = summ(rel, "sikap")
    tol = rel[rel.sikap == "tolak"]
    by_tema = summ(tol[tol.tema_utama.isin(THEMES)], "tema_utama")
    by_tema["tema_utama"] = pd.Categorical(by_tema.tema_utama, THEMES)
    by_tema = by_tema.sort_values("tema_utama")
    # per-case theme like share, to check whether a single viral comment drives a theme
    top = el.sort_values("likeCount", ascending=False)
    n1 = max(1, int(len(el) * 0.01))
    overall = {
        "n_lolos_kualitas": len(el),
        "median_like": float(el.likeCount.median()),
        "mean_like": round(el.likeCount.mean(), 2),
        "max_like": int(el.likeCount.max()),
        "pct_nol_like": round((el.likeCount == 0).mean() * 100, 1),
        "gini_like": round(gini(el.likeCount), 3),
        "pct_like_dari_top1pct_komentar": round(top.head(n1).likeCount.sum() / el.likeCount.sum() * 100, 1),
        "top_level": int((~el.isReply).sum()),
        "pct_top_level_dengan_balasan": round((el[~el.isReply].totalReplyCount > 0).mean() * 100, 1),
        "median_balasan_jika_ada": float(el[~el.isReply & (el.totalReplyCount > 0)].totalReplyCount.median()),
        "max_balasan": int(el.totalReplyCount.max()),
        "top10_like_sikap": top[top.relevant == "y"].head(10).sikap.value_counts().to_dict(),
        "top10_like_tema": top[top.sikap == "tolak"].head(10).tema_utama.value_counts().to_dict(),
    }
    return by_sikap, by_tema, overall


def log_odds(df, group_col, groups, stop, k=15, min_count=5):
    """Weighted log-odds ratio with informative Dirichlet prior (Monroe et al. 2008)."""
    tol = df[df.eligible & (df.sikap == "tolak")]
    counts = {}
    for g in groups:
        c = Counter()
        for t in tol[tol[group_col] == g].text_repr_a.fillna(""):
            c.update(w for w in t.split() if w not in stop and not re.fullmatch(r"\d+", w))
        counts[g] = c
    prior = counts[groups[0]] + counts[groups[1]]
    a0 = sum(prior.values())
    out = []
    for g, h in [(groups[0], groups[1]), (groups[1], groups[0])]:
        yi, yj = counts[g], counts[h]
        ni, nj = sum(yi.values()), sum(yj.values())
        rows = []
        for w, aw in prior.items():
            if aw < min_count:
                continue
            d = (np.log((yi[w] + aw) / (ni + a0 - yi[w] - aw))
                 - np.log((yj[w] + aw) / (nj + a0 - yj[w] - aw)))
            var = 1 / (yi[w] + aw) + 1 / (yj[w] + aw)
            rows.append((w, d / np.sqrt(var), yi[w], yj[w]))
        rows.sort(key=lambda r: -r[1])
        for rank, (w, z, a, b) in enumerate(rows[:k], 1):
            out.append({"perbandingan": group_col, "kelompok": g, "rank": rank, "kata": w,
                        "z": round(z, 2), "n_kelompok": a, "n_lawan": b})
    return pd.DataFrame(out)


def top_terms(df, stop, k=20):
    tol = df[df.eligible & (df.sikap == "tolak")]
    c, dfreq = Counter(), Counter()
    for t in tol.text_repr_a.fillna(""):
        ws = [w for w in t.split() if w not in stop and not re.fullmatch(r"\d+", w)]
        c.update(ws)
        dfreq.update(set(ws))
    return pd.DataFrame([{"rank": i, "kata": w, "frekuensi": n,
                          "pct_komentar_tolak": round(dfreq[w] / len(tol) * 100, 1)}
                         for i, (w, n) in enumerate(c.most_common(k), 1)])


def style(ax):
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.set_facecolor(SURFACE)


def fig_temporal(df):
    el = df[df.eligible]
    fig, ax = plt.subplots(figsize=(7.5, 4.2), facecolor=SURFACE)
    style(ax)
    ax.grid(axis="y", color=GRID, lw=0.6)
    xs = np.logspace(-2, np.log10(max(el.days.max(), 1200)), 400)
    for vt, col in [("third_party", BLUE), ("reupload_archive", ORANGE)]:
        d = np.sort(el[el.video_type == vt].days.values)
        y = np.searchsorted(d, xs, side="right") / len(d) * 100
        ax.plot(xs, y, color=col, lw=2, label=f"{VT[vt]} (n={len(d):,})".replace(",", "."))
        i = np.searchsorted(xs, 7)
        ax.annotate(f"{y[i]:.0f}%", (xs[i], y[i]), xytext=(-30, 8), textcoords="offset points",
                    fontsize=8, color=INK2)
    ax.axvline(7, color=INK2, lw=0.8, ls=":")
    ax.text(7, 102, "7 hari", fontsize=8, color=INK2, ha="center")
    ax.set_xscale("log")
    ax.set_xticks([0.042, 1, 7, 30, 365])
    ax.set_xticklabels(["1 jam", "1 hari", "7 hari", "30 hari", "1 tahun"])
    ax.minorticks_off()
    ax.set_ylim(0, 105)
    ax.set_ylabel("% kumulatif komentar", color=INK2, fontsize=9)
    ax.set_xlabel("Waktu sejak video diunggah (skala log)", color=INK2, fontsize=9)
    ax.set_title("Kapan komentar masuk, menurut jenis video", loc="left", color=INK, fontsize=11)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.text(0.01, 0.01, "Komentar lolos pemeriksaan kualitas (n=3.145).", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fig6_temporal.png", dpi=300)
    plt.close(fig)


def fig_engagement(by_tema):
    t = by_tema.copy()
    fig, ax = plt.subplots(figsize=(7.5, 4.4), facecolor=SURFACE)
    style(ax)
    ax.grid(axis="x", color=GRID, lw=0.6)
    y = np.arange(len(t))
    h = 0.38
    ax.barh(y - h / 2, t.pct_komentar, h - 0.04, color=BLUE, label="% komentar")
    ax.barh(y + h / 2, t.pct_like, h - 0.04, color=ORANGE, label="% like")
    for yi, a, b in zip(y, t.pct_komentar, t.pct_like):
        ax.text(max(a, b) + 0.8, yi, f"{a:.1f} / {b:.1f}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{NAMES[c]} ({c})" for c in t.tema_utama], fontsize=9, color=INK)
    ax.invert_yaxis()
    ax.set_xlabel("% dari komentar tolak / % dari total like komentar tolak", color=INK2, fontsize=9)
    ax.set_title("Porsi komentar vs porsi like per tema utama", loc="left", color=INK, fontsize=11)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.text(0.01, 0.01, "Komentar tolak (n=1.624, tanpa LT). Like hanya konteks, bukan bobot prevalensi.",
             fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fig7_engagement_tema.png", dpi=300)
    plt.close(fig)


def md_table(t):
    t = t.astype(str)
    return "\n".join(["| " + " | ".join(t.columns) + " |", "|" + "---|" * len(t.columns)]
                     + ["| " + " | ".join(r) + " |" for r in t.values])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df, vids = load()
    stop = set(Path("resources/stopwords_bertopic_v1.txt").read_text(encoding="utf-8").split())

    kar, users = characteristics(df, vids)
    tem_vid, sik_per, tem_per = temporal(df, vids)
    eng_sik, eng_tem, eng = engagement(df)
    lo = pd.concat([log_odds(df, "org_type", ["government", "commercial"], stop),
                    log_odds(df, "video_type", ["third_party", "reupload_archive"], stop)])
    terms = top_terms(df, stop)

    kar.to_csv(OUT / "tabel_karakteristik_kasus.csv", index=False)
    tem_vid.to_csv(OUT / "tabel_temporal_video.csv", index=False)
    sik_per.to_csv(OUT / "tabel_sikap_per_periode.csv", index=False)
    tem_per.to_csv(OUT / "tabel_tema_per_periode.csv", index=False)
    eng_sik.to_csv(OUT / "tabel_engagement_sikap.csv", index=False)
    eng_tem.to_csv(OUT / "tabel_engagement_tema.csv", index=False)
    lo.to_csv(OUT / "tabel_istilah_khas.csv", index=False)
    terms.to_csv(OUT / "tabel_istilah_teratas.csv", index=False)
    fig_temporal(df)
    fig_engagement(eng_tem)

    summary = {"script": f"src/descriptive_stats.py v{VERSION}", "pengguna": users, "engagement": eng}
    (OUT / "ringkasan_deskriptif.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                                                   encoding="utf-8")
    lo_wide = lo.groupby(["perbandingan", "kelompok"]).apply(
        lambda g: ", ".join(f"{w} ({z})" for w, z in zip(g.kata, g.z)), include_groups=False).reset_index()
    lo_wide.columns = ["perbandingan", "kelompok", "kata khas (z)"]
    md = ["# Statistik deskriptif (TK3 kriteria 2)", "",
          f"Dibuat oleh `src/descriptive_stats.py` v{VERSION}. Unit: komentar lolos pemeriksaan kualitas "
          "(n=3.145) kecuali disebut lain.", "",
          "## 1. Karakteristik dataset dan pengguna per kasus", "", md_table(kar), "",
          "Ringkasan pengguna: " + json.dumps(users, ensure_ascii=False), "",
          "## 2. Pola temporal per video", "", md_table(tem_vid), "",
          "### Sikap per periode (komentar relevan, % baris)", "", md_table(sik_per), "",
          "### Tema utama per periode (komentar tolak, % baris)", "", md_table(tem_per), "",
          "## 3. Engagement", "", "Ringkasan: " + json.dumps(eng, ensure_ascii=False), "",
          "### Per sikap (komentar relevan)", "", md_table(eng_sik), "",
          "### Per tema utama (komentar tolak)", "", md_table(eng_tem), "",
          "## 4. Karakteristik konten (komentar tolak, `text_repr_a` tanpa stopword)", "",
          "### Kata teratas", "", md_table(terms), "",
          "### Kata khas per kelompok (weighted log-odds, prior Dirichlet informatif; z > 1,96 ≈ signifikan)",
          "", md_table(lo_wide), ""]
    (OUT / "tabel_deskriptif.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Output in {OUT}")


if __name__ == "__main__":
    main()
