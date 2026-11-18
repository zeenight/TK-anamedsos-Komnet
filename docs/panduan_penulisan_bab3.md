# Panduan Penulisan Bab 3: Hasil Penelitian

Dokumen induk untuk Bab 3 (Hasil). Setiap analisis baru untuk Bab 3 dicatat di sini: angka, gambar, file sumber, dan cara menuliskannya. Bab 2 (Metodologi) punya panduan sendiri di `docs/panduan_penulisan_bab2.md`; dokumen ini tidak mengubahnya.

- **Acuan tugas:** TK3 *Data Analytics* (`docs/course/TK-3--Data-Analysis.pdf`), bagian 4.5 Hasil Penelitian. Tenggat 2 Desember 2026, 23:59, format PDF dengan template ACM.
- **Panjang yang direkomendasikan:** 800–1.000 kata.
- **Paket untuk penulis:** `docs/paket_penulisan_hasil/` (gambar, tabel, codebook). Angka di dokumen ini harus sama dengan `tabel/tabel_final.md` di paket itu.

## Status

| Sub-bab | Isi | Status | Sumber |
|---|---|---|---|
| 3.1 | Statistik deskriptif (karakteristik dataset, temporal, engagement, user, konten) | Siap ditulis (2026-11-18) | `experiments/descriptive_v1/`, `fig6`, `fig7` |
| 3.2 | RQ1: tema keberatan | Siap ditulis | `tabel_rq1_tema.csv`, `fig1` |
| 3.3 | RQ2: pemerintah vs komersial | Siap ditulis | `tabel_rq2_org_type.csv`, `tabel_rq2_per_video_type.csv`, `fig2` |
| 3.4 | RQ3: jenis video | Siap ditulis | `tabel_rq3_video_type.csv`, `fig3` |
| 3.5 | Variasi antarkasus dan robustness | Siap ditulis (robustness diperbarui 2026-11-09) | `tabel_per_kasus.csv`, `tabel_robustness.csv`, `fig4` |
| 3.6 | Tema yang muncul bersamaan | Siap ditulis | `tabel_kookurensi.csv`, `fig5` |
| 3.7 | Hasil evaluasi (reliabilitas label, sentimen vs sikap) | Siap ditulis (confusion matrix 2026-11-18) | `validasi_*_hasil.json`, `experiments/sentiment_eval_v1/`, `fig8` |

## Aturan menulis Bab 3

- **Hasil ≠ Diskusi.** TK3 meminta Bab Hasil melaporkan observasi, sedangkan interpretasi rinci dan perbandingan dengan penelitian terdahulu ditulis di Bab Diskusi. Bagian yang ditandai **→ Diskusi** di bawah dipindahkan ke sana.
- Susun berdasarkan pertanyaan penelitian (RQ1, RQ2, RQ3).
- Pakai kala lampau dan angka yang bisa ditelusuri ke file sumber.
- **Tidak ada klaim kausal** dan tidak ada klaim bahwa korpus mewakili masyarakat Indonesia. Tulis "komentar pada kasus pemerintah lebih sering…", jangan "karena pemerintah, warganet…".
- Setiap gambar dan tabel punya caption informatif dan dirujuk di teks. Jelaskan apa yang tersirat, jangan hanya mengulang angka di gambar.
- **Jangan kutip komentar verbatim.** TK2 §3.6 menyatakan laporan hanya menyajikan agregat, karena data bersifat pseudonim dan teks asli bisa dicari ulang. Pakai parafrase singkat tanpa identitas akun. Contoh komentar di tabel bab ini hanya untuk tim, bukan untuk disalin ke laporan.
- Istilah baku mengikuti bagian 5 di `paket_penulisan_hasil/panduan_penulisan_hasil.md` (keberatan / komentar `tolak`, tema utama, kasus pemerintah, video pihak ketiga, κ buta, …).

Corong data untuk pembuka bab (rinciannya di Bab 2):

| Tahap | Komentar |
|---|---|
| Dikumpulkan | 3.307 (8 video, 7 kasus) |
| Lolos pemeriksaan kualitas | 3.145 |
| Relevan dengan penggunaan GenAI | 2.288 (72,8%) |
| Sikap `tolak` (dikode tema) | 1.627 (71,1% dari yang relevan) |

**Selaras dengan TK2** (`docs/course/TK2-Komnet.pdf`). Hal yang berubah atau keliru di TK2 harus ditulis terang-terangan di TK3:

| Hal | Di TK2 | Di TK3 |
|---|---|---|
| Verifikasi | 2 kasus media kredibel, 5 dugaan | 4 terverifikasi (C01, C02, C04 media; C07 pernyataan resmi), 3 belum (C03, C05, C06) |
| Subset robustness | C01–C02 | C02, C04, C07 vs C01 (n=985), lihat 3.5 |
| Tabel 2 (corong) | kolom "Keluar" bergeser (relevansi kosong, sikap 857, tema 661) | relevansi keluar 857, sikap keluar 661, tema 0 |
| Jumlah author | 2.626 (basis 3.307) | 2.545 (basis 3.145); sebutkan basisnya |
| Istilah | "unggahan ulang/arsip" | label gambar "Re-upload/arsip"; pilih satu istilah di teks |
| Repo | https://github.com/zeenight/TK-anamedsos-Komnet (publik) | sama; perlu diperbarui dengan skrip TK3 |

---

## 3.1 Statistik deskriptif → Gambar 6 (`fig6_temporal.png`), Gambar 7 (`fig7_engagement_tema.png`)

Sumber: `experiments/descriptive_v1/` (dibuat oleh `src/descriptive_stats.py`; semua tabel juga ada di `tabel_deskriptif.md`). Unit: 3.145 komentar yang lolos pemeriksaan kualitas, kecuali disebut lain. Ukuran dipilih karena berkaitan dengan RQ (rubrik kriteria 2), bukan untuk melaporkan semua statistik.

**a. Karakteristik dataset dan pengguna** (`tabel_karakteristik_kasus.csv`)

| Kasus | Tipe org | Jenis video | Lolos kualitas | Relevan | Tolak | % balasan | Author unik | Komentar/author |
|---|---|---|---|---|---|---|---|---|
| C01 | komersial | pihak ketiga | 630 | 457 | 276 | 31,3 | 526 | 1,20 |
| C02 | pemerintah | pihak ketiga | 135 | 92 | 65 | 34,1 | 113 | 1,19 |
| C03 | pemerintah | re-upload/arsip | 698 | 563 | 493 | 15,9 | 612 | 1,14 |
| C04 | pemerintah | pihak ketiga | 538 | 306 | 187 | 20,1 | 488 | 1,10 |
| C05 | komersial | re-upload/arsip | 111 | 82 | 77 | 19,8 | 92 | 1,21 |
| C06 | komersial | re-upload/arsip | 115 | 91 | 72 | 29,6 | 95 | 1,21 |
| C07 | pemerintah | pihak ketiga | 918 | 697 | 457 | 33,6 | 709 | 1,29 |
| **Total** | | | **3.145** | **2.288** | **1.627** | **26,3** | **2.545** | **1,24** |

- Total *view* kedelapan video saat pengambilan: 1,6 juta.
- 87,4% author hanya menulis satu komentar. 1% author teraktif menyumbang 7,7% komentar; satu author menulis 43 komentar. Hanya 84 author (3,3%) berkomentar di lebih dari satu kasus.
- **Kaitan dengan RQ:** korpus tidak seimbang (C07 dan C03 = 51% komentar lolos kualitas; komersial didominasi C01), jadi perbandingan RQ2/RQ3 memakai proporsi, bukan hitungan. Sebaran author yang lebar berarti hasil tidak didominasi segelintir akun, tetapi komentar tetap tidak sepenuhnya independen (balasan dalam satu utas, author berulang). Ini alasan uji chi-square hanya dibaca deskriptif.

**b. Pola temporal → Gambar 6** (`tabel_temporal_video.csv`, `tabel_sikap_per_periode.csv`, `tabel_tema_per_periode.csv`)

| Video (kasus) | Jenis | Diunggah | Median hari setelah unggah | % ≤7 hari | % ≤30 hari |
|---|---|---|---|---|---|
| IXNas_31uvQ (C01) | pihak ketiga | 2023-09-29 | 11,2 | 45,9 | 64,0 |
| 1seDwa5-muc (C01) | pihak ketiga | 2023-10-09 | 124,9 | 19,4 | 26,4 |
| ntAyLy0ef-A (C02) | pihak ketiga | 2025-02-22 | 4,4 | 58,5 | 94,1 |
| P4UNSiQ4KbU (C04) | pihak ketiga | 2025-07-03 | 5,7 | 64,5 | 95,5 |
| u40TLtWSY0Q (C07) | pihak ketiga | 2025-03-14 | 1,0 | 86,4 | 96,1 |
| LGSzx-_ggi4 (C03) | re-upload/arsip | 2025-02-18 | 38,6 | 2,9 | 31,5 |
| Ih2mEx2H4Ng (C05) | re-upload/arsip | 2025-03-16 | 23,4 | 16,2 | 60,4 |
| kGTlkh8wKx0 (C06) | re-upload/arsip | 2025-03-04 | 35,7 | 8,7 | 40,9 |

- Video pihak ketiga menerima 67% komentarnya dalam 7 hari pertama; video re-upload/arsip baru 5%. Komentar pada re-upload datang bergelombang 2–8 minggu setelah unggah.
- Sikap stabil antarperiode: di video pihak ketiga `tolak` 63,5% (≤7 hari) vs 63,3% (>7 hari); di re-upload 90,9% vs 87,0%.
- Komposisi tema di video pihak ketiga juga stabil (selisih ≤6 poin). Di re-upload, komentar awal lebih banyak KO (37,5% vs 14,8%) dan lebih sedikit KV (27,5% vs 42,7%), tetapi komentar awalnya hanya 40, jadi jangan ditekankan.
- **Kaitan dengan RQ3:** kedua jenis video berbeda bukan hanya dari pengunggahnya, tetapi juga dari kapan penonton datang. Bahwa komentar re-upload datang setelah video tersebar di luar kanal asal adalah dugaan yang tidak bisa diverifikasi dari data → **Diskusi**.

**c. Engagement → Gambar 7** (`tabel_engagement_sikap.csv`, `tabel_engagement_tema.csv`)

- Like sangat timpang: 65,6% komentar tidak punya like, median 0, Gini 0,951, dan 1% komentar teratas memegang 64,1% seluruh like. Hanya 11,6% komentar top-level yang punya balasan.
- Per sikap (komentar relevan): `tolak` = 71,1% komentar tetapi 90,0% like; `dukung` = 6,6% komentar dan 0,8% like.
- Per tema (komentar tolak): KV 28,8% komentar vs 41,4% like; AK 13,7% vs 3,9%; EJ 9,6% vs 1,5%. AU (6,2% vs 13,5%) dan HC (3,1% vs 8,3%) tampak "disukai", tetapi **79% like AU dan 70% like HC berasal dari satu komentar**; di KV, 33% dari satu komentar.
- **Cara menulis:** like adalah konteks, bukan bobot prevalensi tema (keputusan desain, lihat Bab 2). Tulis bahwa keberatan mendapat like jauh lebih banyak daripada komentar yang membela, dan bahwa keberatan kualitas visual paling banyak disukai, dengan catatan konsentrasi like.

**d. Karakteristik konten** (`tabel_istilah_teratas.csv`, `tabel_istilah_khas.csv`; komentar tolak, `text_repr_a` tanpa stopword)

- Kata teratas: ai (52,4% komentar tolak), iklan, pake/pakai, animator (12,2%), animasi, pemerintah, orang, indonesia, lokal, bagus, anggaran.
- Kata khas per kelompok (weighted log-odds dengan prior Dirichlet informatif, Monroe dkk. 2008; z > 1,96):
  - **Pemerintah:** animator (4,16), pemerintah, animasi, indonesia, komdigi, anggaran (2,18), lokal, negara.
  - **Komersial:** art (4,25), gambar, artist, layak, perusahaan, indomie, masalah, seni, cipta (2,52), hak (2,46).
  - **Re-upload/arsip:** anak, kementrian, konten, jahat, serem, burik, malu (didominasi C03, C05, C06).
  - **Pihak ketiga:** tidak ada kata dengan z > 1,96 (teratas: gambar, kerja, bikin, artist).
- **Kaitan dengan RQ2:** kosakata sudah memberi gambaran awal sebelum pengodean tema: pemerintah dikaitkan dengan animator lokal dan anggaran, komersial dengan seni dan hak cipta. Ini konsisten dengan hasil tema di 3.3.

---

## 3.2 RQ1: tema keberatan → Gambar 1 (`fig1_rq1_tema.png`)

| Kode | Tema | % (n=1.627) | Contoh komentar (dari codebook) |
|---|---|---|---|
| KV | Kualitas visual | 28,7 | "menit ke 🤣🤣 tangan nyatu kanan kiri" · "Masih bagusan animasi minecraft indo 💀💀" |
| KO | Kepantasan organisasi | 21,9 | "Pke ai bukan inovasi tp kemunduran" |
| PK | Pekerja kreatif | 16,8 | "Mengapa iklan pemerintah harus pakai ai padahal ada animator lokal😂" |
| AK | Biaya, anggaran & korupsi | 13,6 | "pff anggaran tinggi hasilnya ai🖐️😂🖐️" |
| EJ | Ejekan tanpa alasan | 9,6 | "sangat layak dihujat" |
| AU | Kekhawatiran umum tentang AI | 6,1 | "Kaya seolah olah ada entitas lain nya mengganti kan manusia serem" |
| HC | Hak cipta | 3,1 | "AI itu cuma nyomot hasil karya orang lain tanpa ngasih royalti ke kreator" |
| LT | Lainnya | 0,2 | (3 komentar) |

Interval kepercayaan Wilson 95% ada di `tabel_rq1_tema.csv`.

**Observasi:** empat tema terbesar masing-masing di atas 13%. Hanya 9,6% komentar yang menolak tanpa alasan. Semua tema yang diharapkan proposal muncul, ditambah dua tema baru (biaya/anggaran/korupsi, kekhawatiran umum AI). Hak cipta kecil (3,1%) dan hampir seluruhnya dari C01.

**→ Diskusi:** keberatan bukan satu kategori "anti-AI".

---

## 3.3 RQ2: pemerintah vs komersial → Gambar 2 (`fig2_rq2_org_type.png`)

| Tema | Pemerintah (n=1.202) | Komersial (n=425) | Selisih (poin) |
|---|---|---|---|
| Kualitas visual | 25,9 | 36,7 | −10,8 |
| Kepantasan organisasi | 25,4 | 12,0 | **+13,4** |
| Pekerja kreatif | 18,3 | 12,5 | +5,8 |
| Biaya, anggaran & korupsi | 15,1 | 9,6 | +5,5 |
| Ejekan tanpa alasan | 8,8 | 11,8 | −3,0 |
| Kekhawatiran umum AI | 5,2 | 8,7 | −3,5 |
| Hak cipta | 1,3 | 8,0 | −6,7 |

χ² = 106,4; df = 6; Cramér's V = 0,256. Angka ini **deskriptif**: komentar mengelompok di 7 kasus, sehingga nilai p terlalu optimistis.

**Stratifikasi per jenis video** (`tabel_rq2_per_video_type.csv`). Jenis organisasi dan jenis video tumpang tindih, jadi perbandingannya juga dilakukan di dalam setiap jenis video:
- Di video pihak ketiga, kepantasan organisasi pemerintah 31,5% vs komersial 10,5%, dan anggaran 20,3% vs 12,0%.
- Di video re-upload/arsip, satu-satunya selisih besar adalah kualitas visual (37,5% vs 55,7%).

**Observasi:** kasus pemerintah lebih sering menyasar organisasinya (kepantasan, uang). Kasus komersial lebih sering menyasar hasilnya (kualitas visual, hak cipta). Selisih kualitas visual sebagian besar berasal dari C05 dan C06 (lihat 3.5).

---

## 3.4 RQ3: jenis video → Gambar 3 (`fig3_rq3_video_type.png`)

| Tema | Pihak ketiga (n=985) | Re-upload/arsip (n=642) | Selisih |
|---|---|---|---|
| Kualitas visual | 20,2 | 41,7 | −21,5 |
| Kepantasan organisasi | 25,6 | 16,2 | +9,4 |
| Biaya, anggaran & korupsi | 18,0 | 7,0 | +11,0 |
| Ejekan tanpa alasan | 5,7 | 15,6 | −9,9 |
| Pekerja kreatif | 17,9 | 15,1 | +2,8 |
| Kekhawatiran umum AI | 7,6 | 3,9 | +3,7 |
| Hak cipta | 4,8 | 0,5 | +4,3 |

χ² = 186,2; df = 6; Cramér's V = 0,339 (deskriptif).

**Observasi:** komentar di video re-upload lebih banyak tentang tampilan dan lebih sering berupa ejekan tanpa alasan. Komentar di video pihak ketiga lebih sering membawa argumen: kepantasan, anggaran, hak cipta.

**Wajib disebut:** tidak ada video unggahan resmi di korpus, jadi RQ3 hanya membandingkan dua dari tiga jenis video di proposal.

**→ Diskusi:** dugaan bahwa *framing* video pihak ketiga mendorong komentar berargumen. Ini tidak diuji, jadi tulis sebagai kemungkinan.

---

## 3.5 Variasi antarkasus dan robustness → Gambar 4 (`fig4_per_kasus.png`)

Gambar 4 adalah peta panas tema × kasus, dengan setiap kolom berjumlah 100%.
- **C05, C06** (filler Ramadan RTV, adzan Mentari TV): 56% kualitas visual.
- **C04** (POLRI): 40% kepantasan organisasi, 23% anggaran.
- **C02** (MBG Komdigi): 35% pekerja kreatif.
- **C07** (animasi AI Komdigi kedua): 30% kepantasan organisasi.
- **C01** (Indomie): satu-satunya kasus dengan hak cipta (12%) dan kekhawatiran umum AI (12%) yang besar.

**Status verifikasi kasus** (dasar subset robustness; tingkat verifikasi mengikuti proposal):

| Kasus | Status | Bukti |
|---|---|---|
| C01 Indomie | Media kredibel | Suara.com (2023) [11] |
| C02 MBG Komdigi | Media kredibel | Tempo [9], [10] |
| C04 POLRI "Pahlawan Masa Kini" | Media kredibel | Suara.com, 23 Juni 2025: video dirilis Divisi Humas Polri di akun X resmi, 22 Juni 2025 [ISI nomor referensi] |
| C07 Animasi AI Komdigi (Maret 2025) | Pernyataan resmi | Diunggah di Instagram Menteri Komdigi Meutya Hafid; keterangan di akhir video menyatakan animasi dibuat dengan AI [ISI link/tanggal unggahan] |
| C03, C05, C06 | Belum terverifikasi | Hanya dari isi video dan komentar |

**Robustness check** (`tabel_robustness.csv`, dijalankan ulang 2026-11-09): hanya kasus terverifikasi, yaitu pemerintah C02, C04, C07 (n=709) vs komersial C01 (n=276). χ² = 128,2; df = 6; Cramér's V = 0,361 (deskriptif).

| Tema | Pemerintah (terverifikasi) | Komersial (C01) | Selisih | Selisih di semua kasus |
|---|---|---|---|---|
| Kepantasan organisasi | 31,5 | 10,5 | **+21,0** | +13,4 |
| Biaya, anggaran & korupsi | 20,3 | 12,0 | +8,3 | +5,5 |
| Pekerja kreatif | 19,2 | 14,5 | +4,7 | +5,8 |
| Kualitas visual | 17,8 | 26,4 | −8,6 | −10,8 |
| Ejekan tanpa alasan | 3,2 | 12,0 | −8,8 | −3,0 |
| Kekhawatiran umum AI | 6,1 | 11,6 | −5,5 | −3,5 |
| Hak cipta | 2,0 | 12,0 | −10,0 | −6,7 |

- Semua arah selisih sama dengan hasil utama. Selisih kepantasan organisasi dan anggaran membesar.
- Kepantasan organisasi dan anggaran lebih tinggi daripada C01 di **ketiga** kasus pemerintah (KO 16,9 / 39,6 / 30,2 vs 10,5; AK 15,4 / 23,0 / 19,9 vs 12,0). Pekerja kreatif dan kualitas visual **tidak** konsisten (PK: C02 35,4 tetapi C04 5,3; KV: C02 32,3 tetapi C07 12,9).
- Sisi komersial hanya diwakili satu kasus, jadi efek organisasi dan efek kasus tidak bisa dipisahkan sepenuhnya.
- Keempat kasus terverifikasi semuanya video pihak ketiga, jadi RQ3 tidak bisa diuji ulang di subset ini.

**Kalimat kunci:**
> Perbedaan antarkasus sama besarnya dengan perbedaan antarjenis organisasi, sehingga perbandingan RQ2 dan RQ3 perlu dibaca bersama hasil per kasus.

---

## 3.6 Tema yang muncul bersamaan → Gambar 5 (`fig5_kookurensi.png`)

- 152 komentar (9,3%) menyebut dua alasan.
- Pasangan tersering: biaya/anggaran + pekerja kreatif (51), kualitas visual + kepantasan organisasi (22), kualitas visual + pekerja kreatif (20), anggaran + kepantasan organisasi (18).

**→ Diskusi:** argumen soal uang sering dipakai untuk membela pekerja kreatif.

---

## 3.7 Hasil evaluasi

TK3 kriteria 4 meminta bukti kualitas analitik. Hasilnya dilaporkan di sini, sedangkan prosedurnya dijelaskan di Bab 2.

**Reliabilitas pelabelan** (manusia vs Claude, sampel acak buta):

| Tahap | Sampel | κ buta | Setelah adjudikasi: Claude vs final |
|---|---|---|---|
| Relevansi per komentar | 100 | 0,267 | 0,71 |
| Sikap | 99 | 0,235 | 0,757 |
| Tema (validasi, codebook v1.1) | 100 | **0,452** | 0,753 |

Laporkan κ buta sebagai angka reliabilitas utama.

**Kualitas topik BERTopic:** putaran 1 c_v 0,416, diversity 0,961, 32,2% outlier. Putaran 2 c_v 0,399, diversity 0,952, 26,3% outlier.

**Sentimen vs sikap → Gambar 8** (`fig8_confusion_sentimen.png`; sumber `experiments/sentiment_eval_v1/`, dibuat oleh `src/sentiment_eval.py`). Acuan: 100 komentar sampel validasi sikap setelah adjudikasi. Dua model pretrained tanpa data latih tambahan.

| Model | Negatif → tolak: P / R / F1 | Akurasi 3 kelas | Macro-F1 | κ | F1 tolak / lain / dukung |
|---|---|---|---|---|---|
| IndoRoBERTa (`w11wo/indonesian-roberta-base-sentiment-classifier`) | 0,75 / 0,82 / 0,78 | 0,65 | 0,47 | 0,27 | 0,78 / 0,44 / 0,19 |
| XLM-R Twitter (`cardiffnlp/twitter-xlm-roberta-base-sentiment`) | 0,78 / 0,71 / 0,75 | 0,61 | 0,44 | 0,24 | 0,75 / 0,44 / 0,13 |
| Baseline selalu `tolak` | – | 0,66 | – | 0 | – |

- Pemetaan 3 kelas: negatif→tolak, netral→lain, positif→dukung. Sebutkan pemetaan ini secara eksplisit, karena sentimen (nada) dan sikap (posisi terhadap penggunaan AI) bukan konstruk yang sama.
- Akurasi 3 kelas kedua model **tidak lebih baik dari baseline** kelas mayoritas (0,66). Model paling gagal pada `dukung` (F1 0,13–0,19): 4 dari 6 komentar pendukung dibaca negatif oleh IndoRoBERTa, karena pembelaan AI sering ditulis dengan nada menyerang pengkritik.
- 8 dari 66 komentar `tolak` dibaca **positif** oleh IndoRoBERTa (sarkasme, mis. "Kreatif sekali"); XLM-R membaca 15 dari 66 sebagai netral.
- Pada seluruh 2.288 komentar relevan (sikap = label akhir v2, bukan standar emas): IndoRoBERTa menilai 1.319 dari 1.627 komentar `tolak` negatif dan 186 positif; 374 dari 510 komentar `lain` juga dinilai negatif. Tabelnya di `crosstab_sentimen_sikap.csv`.
- Terhadap label buta Zillan (n=99) polanya sama (F1 negatif→tolak 0,82 / 0,77; κ 3 kelas 0,14 / 0,16).
- **Cara menulis:** ini bukti untuk TK3 kriteria 4 bahwa output model pretrained tidak bisa diasumsikan benar, sekaligus alasan empiris memakai pelabelan sikap, bukan sentimen, untuk memilih komentar keberatan. Sentimen tetap dilaporkan sebagai pembanding.

**Pemeriksaan otomatis** (`experiments/auto_check_v1/`): classifier embedding lebih jarang sepakat dengan manusia daripada Claude (sikap 0,53 vs 0,63; tema 0,50 vs 0,55). Hasil ini opsional dan bisa masuk lampiran.

---

## Log perubahan

| Tanggal | Perubahan |
|---|---|
| 2026-11-09 | Dokumen dibuat dari bagian 3 `paket_penulisan_hasil/panduan_penulisan_hasil.md`. Robustness diperbarui: C04 (media kredibel) dan C07 (pernyataan resmi) dihitung terverifikasi. |
| 2026-11-18 | 3.1 statistik deskriptif diisi (`src/descriptive_stats.py`, fig6–fig7). 3.7: confusion matrix dan P/R/F1 sentimen vs sikap (`src/sentiment_eval.py`, fig8). Gambar dan tabel baru disalin ke `paket_penulisan_hasil/`. |
| 2026-11-18 | Diselaraskan dengan TK2 (`docs/course/TK2-Komnet.pdf`): κ relevansi 0,267; larangan kutipan verbatim (TK2 §3.6); tabel "Selaras dengan TK2" (verifikasi, robustness, koreksi Tabel 2 TK2, basis jumlah author, istilah, repo publik). |
