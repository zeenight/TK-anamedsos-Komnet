"""
Final RQ1-RQ3 tables and figures from the v2 theme codes (tema_final_v2.csv).

Output (experiments/themes_v1/hasil_v2/):
  tabel_rq1_tema.csv            n and % of tema_utama, with Wilson 95% CI, plus any-mention counts
  tabel_rq2_org_type.csv        % per org type (government / commercial), CI, difference in points
  tabel_rq3_video_type.csv      % per video type (reupload_archive / third_party), CI, difference
  tabel_per_kasus.csv           % per case (C01-C07)
  tabel_kookurensi.csv          tema_utama x tema_kedua counts (comments with a second theme)
  tabel_robustness.csv          RQ2 again with only verified cases (credible_media or official_disclosure)
  uji_chi2.json                 chi-square + Cramer's V for RQ2/RQ3 (descriptive, see note)
  tabel_final.md                all tables in Markdown for the report
  fig1_rq1_tema.png, fig2_rq2_org_type.png, fig3_rq3_video_type.png, fig4_per_kasus.png, fig5_kookurensi.png

Usage (from the project root):
  python experiments/themes_v1/tabel_grafik_v2.py
"""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DIR = Path(__file__).parent
OUT = DIR / "hasil_v2"
MANIFEST = DIR.parents[1] / "config" / "videos_manifest.csv"

# statuses counted as verified in the robustness check (team decision 2026-11-09:
# official_disclosure = the organisation itself stated the AI use, counted as verified)
VERIFIED = ["credible_media", "official_disclosure"]

THEMES = ["KV", "KO", "PK", "AK", "EJ", "AU", "HC", "LT"]
NAMES = {
    "KV": "Kualitas visual", "KO": "Kepantasan organisasi", "PK": "Pekerja kreatif",
    "AK": "Biaya, anggaran & korupsi", "EJ": "Ejekan tanpa alasan", "AU": "Kekhawatiran umum AI",
    "HC": "Hak cipta", "LT": "Lainnya",
}
GROUPS = {
    "org_type": (["government", "commercial"], {"government": "Pemerintah", "commercial": "Komersial"}),
    "video_type": (["third_party", "reupload_archive"],
                   {"third_party": "Pihak ketiga", "reupload_archive": "Re-upload/arsip"}),
}

# reference palette (dataviz skill, light mode): categorical slots 1-2, text and grid tokens
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SEQ = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def wilson(k, n, z=1.959964):
    p = k / n
    mid = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round((mid - half) * 100, 1), round((mid + half) * 100, 1)


def share_table(df, col, levels):
    rows = []
    for t in THEMES:
        row = {"kode": t, "tema": NAMES[t]}
        for g in levels:
            sub = df[df[col] == g]
            k, n = int((sub["tema_utama"] == t).sum()), len(sub)
            lo, hi = wilson(k, n)
            row.update({f"n_{g}": k, f"pct_{g}": round(k / n * 100, 1), f"ci_{g}": f"{lo}-{hi}"})
        row["selisih_poin"] = round(row[f"pct_{levels[0]}"] - row[f"pct_{levels[1]}"], 1)
        rows.append(row)
    return pd.DataFrame(rows)


def chi2(df, col):
    ct = pd.crosstab(df["tema_utama"], df[col]).drop(index="LT", errors="ignore")
    stat, p, dof, _ = chi2_contingency(ct)
    v = np.sqrt(stat / (ct.values.sum() * (min(ct.shape) - 1)))
    return {"chi2": round(float(stat), 2), "dof": int(dof), "p": float(f"{p:.3g}"), "cramers_v": round(float(v), 3),
            "n": int(ct.values.sum()), "note": "LT excluded (3 comments); comments are clustered in 7 cases, "
            "so p-values overstate certainty and are descriptive only"}


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def fig_rq1(t1, n):
    d = t1.iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.2), facecolor=SURFACE)
    style(ax)
    ax.barh(d["tema"], d["pct"], color=BLUE, height=0.6)
    lo = d["pct"] - d["ci_lo"]
    hi = d["ci_hi"] - d["pct"]
    ax.errorbar(d["pct"], d["tema"], xerr=[lo, hi], fmt="none", ecolor=INK2, elinewidth=1, capsize=3)
    for y, (p, k, h) in enumerate(zip(d["pct"], d["n"], d["ci_hi"])):
        ax.text(h + 0.8, y, f"{p:.1f}% (n={k})", va="center", fontsize=9, color=INK)
    ax.set_xlim(0, d["ci_hi"].max() + 9)
    ax.set_xlabel("% komentar tolak (tema utama)", color=INK2)
    ax.set_title(f"RQ1: Tema keberatan dalam {n:,} komentar tolak".replace(",", "."), loc="left", color=INK,
                 fontsize=12)
    fig.text(0.01, 0.01, "Garis: interval kepercayaan Wilson 95%.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fig1_rq1_tema.png", dpi=300)
    plt.close(fig)


def fig_group(tab, col, title, fname, df):
    levels, labels = GROUPS[col]
    d = tab[tab["kode"] != "LT"].iloc[::-1].reset_index(drop=True)
    y = np.arange(len(d))
    h = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 4.6), facecolor=SURFACE)
    style(ax)
    for i, (g, c) in enumerate(zip(levels, [BLUE, ORANGE])):
        n = int((df[col] == g).sum())
        off = h / 2 + 0.02 if i == 0 else -(h / 2 + 0.02)
        ax.barh(y + off, d[f"pct_{g}"], height=h, color=c, label=f"{labels[g]} (n={n})")
        for yy, p in zip(y + off, d[f"pct_{g}"]):
            ax.text(p + 0.5, yy, f"{p:.1f}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(y, d["tema"])
    ax.set_xlabel("% komentar tolak dalam kelompok", color=INK2)
    ax.set_xlim(0, max(d[f"pct_{levels[0]}"].max(), d[f"pct_{levels[1]}"].max()) + 6)
    ax.legend(frameon=False, loc="lower right", fontsize=9, labelcolor=INK)
    ax.set_title(title, loc="left", color=INK, fontsize=12)
    fig.text(0.01, 0.01, "Lainnya (LT, 3 komentar) tidak ditampilkan.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / fname, dpi=300)
    plt.close(fig)


def fig_heat(mat, fname, title, xlabel, ylabels, fmt, note, vmax=None):
    fig, ax = plt.subplots(figsize=(8.5, 4.8), facecolor=SURFACE)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("seq", SEQ)
    vmax = vmax or mat.values.max()
    ax.imshow(mat.values, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(mat.shape[1]), mat.columns, color=INK2)
    ax.set_yticks(range(mat.shape[0]), ylabels, color=INK2)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(mat.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(mat.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.tick_params(which="minor", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat.values[i, j]
            ax.text(j, i, fmt(v), ha="center", va="center", fontsize=8.5,
                    color="white" if v > vmax * 0.55 else INK)
    ax.set_xlabel(xlabel, color=INK2)
    ax.set_title(title, loc="left", color=INK, fontsize=12)
    fig.text(0.01, 0.01, note, fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / fname, dpi=300)
    plt.close(fig)


def md(df):
    return df.to_markdown(index=False)


def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DIR / "tema_final_v2.csv")
    man = pd.read_csv(MANIFEST).drop_duplicates("case_id").set_index("case_id")
    df["verification_status"] = df["case_id"].map(man["verification_status"])
    n = len(df)

    # RQ1
    t1 = df["tema_utama"].value_counts().reindex(THEMES, fill_value=0).rename("n").reset_index()
    t1.columns = ["kode", "n"]
    t1.insert(1, "tema", t1["kode"].map(NAMES))
    t1["pct"] = (t1["n"] / n * 100).round(1)
    ci = [wilson(k, n) for k in t1["n"]]
    t1["ci_lo"], t1["ci_hi"] = [c[0] for c in ci], [c[1] for c in ci]
    t1["disebut_sbg_tema_kedua"] = t1["kode"].map(df["tema_kedua"].value_counts()).fillna(0).astype(int)
    t1["disebut_total"] = t1["n"] + t1["disebut_sbg_tema_kedua"]
    t1.to_csv(OUT / "tabel_rq1_tema.csv", index=False)

    # RQ2 / RQ3
    t2 = share_table(df, "org_type", GROUPS["org_type"][0])
    t3 = share_table(df, "video_type", GROUPS["video_type"][0])
    t2.to_csv(OUT / "tabel_rq2_org_type.csv", index=False)
    t3.to_csv(OUT / "tabel_rq3_video_type.csv", index=False)
    tests = {"rq2_org_type": chi2(df, "org_type"), "rq3_video_type": chi2(df, "video_type")}

    # per case
    cases = sorted(df["case_id"].unique())
    pc = pd.crosstab(df["tema_utama"], df["case_id"], normalize="columns").reindex(THEMES, fill_value=0) * 100
    pc = pc.round(1)
    info = df.groupby("case_id").agg(n=("idx", "size"), org_type=("org_type", "first"),
                                     video_type=("video_type", "first"),
                                     verifikasi=("verification_status", "first"))
    tc = pc.T.join(info)[["org_type", "video_type", "verifikasi", "n"] + THEMES].reset_index()
    tc.to_csv(OUT / "tabel_per_kasus.csv", index=False)

    # RQ2 within each video type (org type and video type overlap: reupload = C03 vs C05/C06)
    strata = []
    for vt in GROUPS["video_type"][0]:
        sub = df[df["video_type"] == vt]
        t = share_table(sub, "org_type", GROUPS["org_type"][0])
        t.insert(0, "video_type", vt)
        strata.append(t)
        tests[f"rq2_within_{vt}"] = chi2(sub, "org_type")
    ts = pd.concat(strata)
    ts.to_csv(OUT / "tabel_rq2_per_video_type.csv", index=False)

    # co-occurrence
    two = df.dropna(subset=["tema_kedua"])
    co = pd.crosstab(two["tema_utama"], two["tema_kedua"]).reindex(index=THEMES, columns=THEMES, fill_value=0)
    co = co.loc[(co.sum(axis=1) > 0), (co.sum(axis=0) > 0)]
    co.to_csv(OUT / "tabel_kookurensi.csv")
    pairs = two.apply(lambda r: "+".join(sorted([r["tema_utama"], r["tema_kedua"]])), axis=1).value_counts()

    # robustness: verified cases only
    cred = df[df["verification_status"].isin(VERIFIED)]
    cred_cases = {g: sorted(cred.loc[cred["org_type"] == g, "case_id"].unique()) for g in GROUPS["org_type"][0]}
    cred_vt = sorted(cred["video_type"].unique())
    tr = share_table(cred, "org_type", GROUPS["org_type"][0])
    tr = tr.merge(t2[["kode", "pct_government", "pct_commercial", "selisih_poin"]], on="kode",
                  suffixes=("", "_semua"))
    tr.to_csv(OUT / "tabel_robustness.csv", index=False)
    tests["robustness_org_type_verified_only"] = chi2(cred, "org_type")
    (OUT / "uji_chi2.json").write_text(json.dumps(tests, indent=2), encoding="utf-8")

    # figures
    fig_rq1(t1[t1["kode"] != "LT"], n)
    fig_group(t2, "org_type", "RQ2: Komposisi tema, pemerintah vs komersial", "fig2_rq2_org_type.png", df)
    fig_group(t3, "video_type", "RQ3: Komposisi tema per jenis video", "fig3_rq3_video_type.png", df)
    heat = pc.drop(index="LT")
    xl = [f"{c}\n{'Pem.' if info.loc[c, 'org_type'] == 'government' else 'Kom.'}\nn={info.loc[c, 'n']}"
          for c in heat.columns]
    fig_heat(heat.set_axis(xl, axis=1), "fig4_per_kasus.png", "Komposisi tema per kasus (% kolom)", "",
             [NAMES[t] for t in heat.index], lambda v: f"{v:.0f}",
             "Pem. = pemerintah, Kom. = komersial. Setiap kolom berjumlah 100% (LT tidak ditampilkan).")
    fig_heat(co, "fig5_kookurensi.png", f"Tema utama x tema kedua ({len(two)} komentar dengan dua alasan)",
             "tema kedua", [f"{NAMES[t]} ({t})" for t in co.index], lambda v: f"{v:.0f}" if v else "",
             "Baris = tema utama, kolom = tema kedua; angka = jumlah komentar.")

    # markdown
    show = lambda t, lv: t[["kode", "tema"] + [c for g in lv for c in (f"n_{g}", f"pct_{g}", f"ci_{g}")]
                           + ["selisih_poin"]]
    parts = [
        "# Tabel final tema keberatan (codebook v2)",
        f"Sumber: `tema_final_v2.csv`, {n} komentar `tolak`. Persentase = tema utama; CI = Wilson 95%. "
        "Selisih = kelompok pertama dikurangi kelompok kedua (poin persentase).",
        "## RQ1: tema keberatan", md(t1),
        f"## RQ2: pemerintah (n={int((df.org_type == 'government').sum())}) vs komersial "
        f"(n={int((df.org_type == 'commercial').sum())})", md(show(t2, GROUPS["org_type"][0])),
        f"Chi-square: {tests['rq2_org_type']}",
        f"## RQ3: pihak ketiga (n={int((df.video_type == 'third_party').sum())}) vs re-upload/arsip "
        f"(n={int((df.video_type == 'reupload_archive').sum())})", md(show(t3, GROUPS["video_type"][0])),
        f"Chi-square: {tests['rq3_video_type']}",
        "Tidak ada video unggahan resmi di korpus, sehingga RQ3 hanya membandingkan dua jenis video.",
        "## RQ2 per jenis video (stratifikasi)",
        "Jenis organisasi dan jenis video tumpang tindih (re-upload/arsip = C03 pemerintah vs C05, C06 komersial; "
        "pihak ketiga = C02, C04, C07 pemerintah vs C01 komersial), jadi RQ2 juga dibandingkan di dalam tiap jenis video.",
        md(ts[["video_type", "kode", "tema", "pct_government", "pct_commercial", "selisih_poin"]]),
        "Chi-square: " + "; ".join(f"{vt}: {tests[f'rq2_within_{vt}']}" for vt in GROUPS["video_type"][0]),
        "## Per kasus (% kolom)", md(tc),
        "## Ko-okurensi (tema utama x tema kedua)", co.to_markdown(),
        "Pasangan tersering (tanpa urutan): " + ", ".join(f"{k} {v}" for k, v in pairs.head(8).items()),
        f"## Robustness: hanya kasus terverifikasi ({', '.join(VERIFIED)}; "
        f"pemerintah {', '.join(cred_cases['government'])}, komersial {', '.join(cred_cases['commercial'])}; "
        f"n={len(cred)})",
        md(tr[["kode", "tema", "pct_government", "pct_commercial", "selisih_poin", "pct_government_semua",
               "pct_commercial_semua", "selisih_poin_semua"]]),
        f"Pada subset ini sisi komersial hanya diwakili {len(cred_cases['commercial'])} kasus, sehingga perbedaan "
        "jenis organisasi dan perbedaan kasus tidak bisa dipisahkan sepenuhnya. Semua kasus terverifikasi berjenis "
        f"video {', '.join(cred_vt)}, jadi RQ3 tidak bisa diuji ulang pada subset ini.",
        f"Chi-square: {tests['robustness_org_type_verified_only']}",
    ]
    (OUT / "tabel_final.md").write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print((OUT / "tabel_final.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
