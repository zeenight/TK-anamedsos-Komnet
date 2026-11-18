# Statistik deskriptif (TK3 kriteria 2)

Dibuat oleh `src/descriptive_stats.py` v1.0. Unit: komentar lolos pemeriksaan kualitas (n=3.145) kecuali disebut lain.

## 1. Karakteristik dataset dan pengguna per kasus

| case_id | org_type | video_type | n_video | views | komentar_terkumpul | lolos_kualitas | relevan | tolak | pct_balasan | author_unik | komentar_per_author | pct_author_1_komentar | pct_komentar_dari_author_3plus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | commercial | third_party | 2 | 586017 | 647 | 630 | 457 | 276 | 31.3 | 526 | 1.2 | 90.3 | 14.8 |
| C02 | government | third_party | 1 | 51848 | 172 | 135 | 92 | 65 | 34.1 | 113 | 1.19 | 87.6 | 8.9 |
| C03 | government | reupload_archive | 1 | 39972 | 730 | 698 | 563 | 493 | 15.9 | 612 | 1.14 | 90.4 | 7.9 |
| C04 | government | third_party | 1 | 138160 | 553 | 538 | 306 | 187 | 20.1 | 488 | 1.1 | 91.8 | 4.5 |
| C05 | commercial | reupload_archive | 1 | 16132 | 127 | 111 | 82 | 77 | 19.8 | 92 | 1.21 | 90.2 | 14.4 |
| C06 | commercial | reupload_archive | 1 | 567978 | 125 | 115 | 91 | 72 | 29.6 | 95 | 1.21 | 85.3 | 13.9 |
| C07 | government | third_party | 1 | 195458 | 953 | 918 | 697 | 457 | 33.6 | 709 | 1.29 | 88.7 | 19.9 |
| Total |  |  | 8 | 1595565 | 3307 | 3145 | 2288 | 1627 | 26.3 | 2545 | 1.24 | 87.4 | 14.7 |

Ringkasan pengguna: {"author_unik": 2545, "author_lebih_dari_1_kasus": 84, "pct_author_lebih_dari_1_kasus": 3.3, "max_komentar_satu_author": 43, "pct_komentar_dari_top1pct_author": 7.7, "pct_author_1_komentar": 87.4}

## 2. Pola temporal per video

| video_id | case_id | video_type | kanal | tanggal_unggah | komentar_pertama | komentar_terakhir | n | median_hari_setelah_unggah | pct_dalam_1_hari | pct_dalam_7_hari | pct_dalam_30_hari | pct_setelah_365_hari |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IXNas_31uvQ | C01 | third_party | Jaret Fajrianto 【GHOSTY's COMIC】 | 2023-09-29 | 2023-09-29 | 2026-09-09 | 558 | 11.2 | 19.9 | 45.9 | 64.0 | 5.6 |
| 1seDwa5-muc | C01 | third_party | Suaradotcom | 2023-10-09 | 2023-10-09 | 2026-03-13 | 72 | 124.9 | 1.4 | 19.4 | 26.4 | 22.2 |
| u40TLtWSY0Q | C07 | third_party | Mindplace | 2025-03-14 | 2025-03-14 | 2026-08-13 | 918 | 1.0 | 50.2 | 86.4 | 96.1 | 0.1 |
| ntAyLy0ef-A | C02 | third_party | Pherfect | 2025-02-22 | 2025-02-23 | 2025-10-29 | 135 | 4.4 | 2.2 | 58.5 | 94.1 | 0.0 |
| LGSzx-_ggi4 | C03 | reupload_archive | Kominfo Muara Enim | 2025-02-18 | 2025-02-19 | 2026-09-23 | 698 | 38.6 | 1.4 | 2.9 | 31.5 | 1.9 |
| P4UNSiQ4KbU | C04 | third_party | Mindplace | 2025-07-03 | 2025-07-03 | 2026-06-05 | 538 | 5.7 | 24.0 | 64.5 | 95.5 | 0.0 |
| Ih2mEx2H4Ng | C05 | reupload_archive | ATCH | 2025-03-16 | 2025-03-16 | 2026-09-14 | 111 | 23.4 | 5.4 | 16.2 | 60.4 | 1.8 |
| kGTlkh8wKx0 | C06 | reupload_archive | ATCH | 2025-03-04 | 2025-03-05 | 2026-08-09 | 115 | 35.7 | 4.3 | 8.7 | 40.9 | 2.6 |

### Sikap per periode (komentar relevan, % baris)

| video_type | periode | dukung | lain | tolak | n |
|---|---|---|---|---|---|
| reupload_archive | <=7 hari | 0.0 | 9.1 | 90.9 | 44 |
| reupload_archive | >7 hari | 0.9 | 12.1 | 87.0 | 692 |
| third_party | <=7 hari | 8.7 | 27.7 | 63.5 | 1067 |
| third_party | >7 hari | 10.7 | 26.0 | 63.3 | 485 |

### Tema utama per periode (komentar tolak, % baris)

| video_type | periode | KV | KO | PK | AK | EJ | AU | HC | n |
|---|---|---|---|---|---|---|---|---|---|
| reupload_archive | <=7 hari | 27.5 | 37.5 | 15.0 | 7.5 | 7.5 | 5.0 | 0.0 | 40 |
| reupload_archive | >7 hari | 42.7 | 14.8 | 15.1 | 7.0 | 16.1 | 3.8 | 0.5 | 602 |
| third_party | <=7 hari | 19.2 | 27.6 | 18.4 | 18.1 | 5.0 | 7.2 | 4.3 | 678 |
| third_party | >7 hari | 22.5 | 21.2 | 16.6 | 17.6 | 7.2 | 8.5 | 5.9 | 307 |

## 3. Engagement

Ringkasan: {"n_lolos_kualitas": 3145, "median_like": 0.0, "mean_like": 5.88, "max_like": 2016, "pct_nol_like": 65.6, "gini_like": 0.951, "pct_like_dari_top1pct_komentar": 64.1, "top_level": 2319, "pct_top_level_dengan_balasan": 11.6, "median_balasan_jika_ada": 1.0, "max_balasan": 38, "top10_like_sikap": {"tolak": 9, "lain": 1}, "top10_like_tema": {"KV": 5, "KO": 2, "AU": 1, "HC": 1, "PK": 1}}

### Per sikap (komentar relevan)

| sikap | n | pct_komentar | total_like | pct_like | median_like | mean_like | p90_like | max_like | pct_like_dari_1_komentar_teratas | pct_nol_like |
|---|---|---|---|---|---|---|---|---|---|---|
| dukung | 151 | 6.6 | 131 | 0.8 | 0.0 | 0.87 | 2.0 | 38 | 29.0 | 74.8 |
| lain | 510 | 22.3 | 1509 | 9.2 | 0.0 | 2.96 | 3.0 | 385 | 25.5 | 67.5 |
| tolak | 1627 | 71.1 | 14766 | 90.0 | 0.0 | 9.08 | 7.0 | 2016 | 13.7 | 61.2 |

### Per tema utama (komentar tolak)

| tema_utama | n | pct_komentar | total_like | pct_like | median_like | mean_like | p90_like | max_like | pct_like_dari_1_komentar_teratas | pct_nol_like |
|---|---|---|---|---|---|---|---|---|---|---|
| KV | 467 | 28.8 | 6116 | 41.4 | 0.0 | 13.1 | 9.0 | 2016 | 33.0 | 56.7 |
| KO | 356 | 21.9 | 2510 | 17.0 | 0.0 | 7.05 | 6.5 | 525 | 20.9 | 59.8 |
| PK | 273 | 16.8 | 2117 | 14.3 | 0.0 | 7.75 | 13.2 | 351 | 16.6 | 55.3 |
| AK | 222 | 13.7 | 574 | 3.9 | 0.0 | 2.59 | 2.0 | 251 | 43.7 | 70.3 |
| EJ | 156 | 9.6 | 228 | 1.5 | 0.0 | 1.46 | 3.0 | 79 | 34.6 | 69.9 |
| AU | 100 | 6.2 | 1990 | 13.5 | 0.0 | 19.9 | 7.1 | 1572 | 79.0 | 70.0 |
| HC | 50 | 3.1 | 1224 | 8.3 | 0.0 | 24.48 | 13.7 | 859 | 70.2 | 60.0 |

## 4. Karakteristik konten (komentar tolak, `text_repr_a` tanpa stopword)

### Kata teratas

| rank | kata | frekuensi | pct_komentar_tolak |
|---|---|---|---|
| 1 | ai | 1220 | 52.4 |
| 2 | iklan | 341 | 16.5 |
| 3 | pake | 335 | 17.4 |
| 4 | animator | 251 | 12.2 |
| 5 | animasi | 206 | 9.9 |
| 6 | pemerintah | 185 | 9.0 |
| 7 | bikin | 181 | 9.3 |
| 8 | pakai | 146 | 7.3 |
| 9 | orang | 128 | 6.6 |
| 10 | indonesia | 127 | 6.6 |
| 11 | lokal | 110 | 6.0 |
| 12 | bagus | 101 | 5.3 |
| 13 | banget | 92 | 5.2 |
| 14 | video | 73 | 3.6 |
| 15 | gambar | 69 | 3.4 |
| 16 | anak | 67 | 3.6 |
| 17 | anggaran | 66 | 3.6 |
| 18 | kerja | 56 | 2.8 |
| 19 | manusia | 55 | 2.6 |
| 20 | marjan | 55 | 3.2 |

### Kata khas per kelompok (weighted log-odds, prior Dirichlet informatif; z > 1,96 ≈ signifikan)

| perbandingan | kelompok | kata khas (z) |
|---|---|---|
| org_type | commercial | art (4.25), gambar (4.03), artist (3.91), layak (3.39), perusahaan (3.35), mi (3.28), indomie (3.19), masalah (3.01), seni (2.69), adzan (2.58), cipta (2.52), mie (2.49), hak (2.46), bolanya (2.39), pocari (2.26) |
| org_type | government | animator (4.16), pemerintah (3.86), animasi (3.02), indonesia (2.69), komdigi (2.48), anggaran (2.18), lokal (2.12), negara (1.98), konten (1.89), lomba (1.81), video (1.8), polisi (1.65), korupsi (1.54), terkait (1.54), bni (1.51) |
| video_type | reupload_archive | anak (3.91), terkait (3.8), kementrian (3.52), tung (3.52), konten (2.84), jahat (2.83), serem (2.75), adzan (2.7), burik (2.58), bola (2.49), bolanya (2.49), pake (2.47), jalan (2.39), malu (2.37), iklan (2.35) |
| video_type | third_party | gambar (1.97), kerja (1.97), bikin (1.94), artist (1.91), masalah (1.61), prompt (1.55), duit (1.53), karya (1.52), art (1.52), polisi (1.49), layak (1.45), lomba (1.42), indo (1.37), ilustrator (1.32), artis (1.32) |
