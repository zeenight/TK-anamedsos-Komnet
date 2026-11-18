# Tabel final tema keberatan (codebook v2)

Sumber: `tema_final_v2.csv`, 1627 komentar `tolak`. Persentase = tema utama; CI = Wilson 95%. Selisih = kelompok pertama dikurangi kelompok kedua (poin persentase).

## RQ1: tema keberatan

| kode   | tema                      |   n |   pct |   ci_lo |   ci_hi |   disebut_sbg_tema_kedua |   disebut_total |
|:-------|:--------------------------|----:|------:|--------:|--------:|-------------------------:|----------------:|
| KV     | Kualitas visual           | 467 |  28.7 |    26.6 |    30.9 |                       27 |             494 |
| KO     | Kepantasan organisasi     | 356 |  21.9 |    19.9 |    24   |                       28 |             384 |
| PK     | Pekerja kreatif           | 273 |  16.8 |    15   |    18.7 |                       54 |             327 |
| AK     | Biaya, anggaran & korupsi | 222 |  13.6 |    12.1 |    15.4 |                       34 |             256 |
| EJ     | Ejekan tanpa alasan       | 156 |   9.6 |     8.3 |    11.1 |                        0 |             156 |
| AU     | Kekhawatiran umum AI      | 100 |   6.1 |     5.1 |     7.4 |                        4 |             104 |
| HC     | Hak cipta                 |  50 |   3.1 |     2.3 |     4   |                        5 |              55 |
| LT     | Lainnya                   |   3 |   0.2 |     0.1 |     0.5 |                        0 |               3 |

## RQ2: pemerintah (n=1202) vs komersial (n=425)

| kode   | tema                      |   n_government |   pct_government | ci_government   |   n_commercial |   pct_commercial | ci_commercial   |   selisih_poin |
|:-------|:--------------------------|---------------:|-----------------:|:----------------|---------------:|-----------------:|:----------------|---------------:|
| KV     | Kualitas visual           |            311 |             25.9 | 23.5-28.4       |            156 |             36.7 | 32.3-41.4       |          -10.8 |
| KO     | Kepantasan organisasi     |            305 |             25.4 | 23.0-27.9       |             51 |             12   | 9.2-15.4        |           13.4 |
| PK     | Pekerja kreatif           |            220 |             18.3 | 16.2-20.6       |             53 |             12.5 | 9.7-16.0        |            5.8 |
| AK     | Biaya, anggaran & korupsi |            181 |             15.1 | 13.1-17.2       |             41 |              9.6 | 7.2-12.8        |            5.5 |
| EJ     | Ejekan tanpa alasan       |            106 |              8.8 | 7.3-10.6        |             50 |             11.8 | 9.0-15.2        |           -3   |
| AU     | Kekhawatiran umum AI      |             63 |              5.2 | 4.1-6.6         |             37 |              8.7 | 6.4-11.8        |           -3.5 |
| HC     | Hak cipta                 |             16 |              1.3 | 0.8-2.2         |             34 |              8   | 5.8-11.0        |           -6.7 |
| LT     | Lainnya                   |              0 |              0   | 0.0-0.3         |              3 |              0.7 | 0.2-2.1         |           -0.7 |

Chi-square: {'chi2': 106.36, 'dof': 6, 'p': 1.18e-20, 'cramers_v': 0.256, 'n': 1624, 'note': 'LT excluded (3 comments); comments are clustered in 7 cases, so p-values overstate certainty and are descriptive only'}

## RQ3: pihak ketiga (n=985) vs re-upload/arsip (n=642)

| kode   | tema                      |   n_third_party |   pct_third_party | ci_third_party   |   n_reupload_archive |   pct_reupload_archive | ci_reupload_archive   |   selisih_poin |
|:-------|:--------------------------|----------------:|------------------:|:-----------------|---------------------:|-----------------------:|:----------------------|---------------:|
| KV     | Kualitas visual           |             199 |              20.2 | 17.8-22.8        |                  268 |                   41.7 | 38.0-45.6             |          -21.5 |
| KO     | Kepantasan organisasi     |             252 |              25.6 | 23.0-28.4        |                  104 |                   16.2 | 13.6-19.2             |            9.4 |
| PK     | Pekerja kreatif           |             176 |              17.9 | 15.6-20.4        |                   97 |                   15.1 | 12.5-18.1             |            2.8 |
| AK     | Biaya, anggaran & korupsi |             177 |              18   | 15.7-20.5        |                   45 |                    7   | 5.3-9.3               |           11   |
| EJ     | Ejekan tanpa alasan       |              56 |               5.7 | 4.4-7.3          |                  100 |                   15.6 | 13.0-18.6             |           -9.9 |
| AU     | Kekhawatiran umum AI      |              75 |               7.6 | 6.1-9.4          |                   25 |                    3.9 | 2.7-5.7               |            3.7 |
| HC     | Hak cipta                 |              47 |               4.8 | 3.6-6.3          |                    3 |                    0.5 | 0.2-1.4               |            4.3 |
| LT     | Lainnya                   |               3 |               0.3 | 0.1-0.9          |                    0 |                    0   | 0.0-0.6               |            0.3 |

Chi-square: {'chi2': 186.18, 'dof': 6, 'p': 1.65e-37, 'cramers_v': 0.339, 'n': 1624, 'note': 'LT excluded (3 comments); comments are clustered in 7 cases, so p-values overstate certainty and are descriptive only'}

Tidak ada video unggahan resmi di korpus, sehingga RQ3 hanya membandingkan dua jenis video.

## RQ2 per jenis video (stratifikasi)

Jenis organisasi dan jenis video tumpang tindih (re-upload/arsip = C03 pemerintah vs C05, C06 komersial; pihak ketiga = C02, C04, C07 pemerintah vs C01 komersial), jadi RQ2 juga dibandingkan di dalam tiap jenis video.

| video_type       | kode   | tema                      |   pct_government |   pct_commercial |   selisih_poin |
|:-----------------|:-------|:--------------------------|-----------------:|-----------------:|---------------:|
| third_party      | KV     | Kualitas visual           |             17.8 |             26.4 |           -8.6 |
| third_party      | KO     | Kepantasan organisasi     |             31.5 |             10.5 |           21   |
| third_party      | PK     | Pekerja kreatif           |             19.2 |             14.5 |            4.7 |
| third_party      | AK     | Biaya, anggaran & korupsi |             20.3 |             12   |            8.3 |
| third_party      | EJ     | Ejekan tanpa alasan       |              3.2 |             12   |           -8.8 |
| third_party      | AU     | Kekhawatiran umum AI      |              6.1 |             11.6 |           -5.5 |
| third_party      | HC     | Hak cipta                 |              2   |             12   |          -10   |
| third_party      | LT     | Lainnya                   |              0   |              1.1 |           -1.1 |
| reupload_archive | KV     | Kualitas visual           |             37.5 |             55.7 |          -18.2 |
| reupload_archive | KO     | Kepantasan organisasi     |             16.6 |             14.8 |            1.8 |
| reupload_archive | PK     | Pekerja kreatif           |             17   |              8.7 |            8.3 |
| reupload_archive | AK     | Biaya, anggaran & korupsi |              7.5 |              5.4 |            2.1 |
| reupload_archive | EJ     | Ejekan tanpa alasan       |             16.8 |             11.4 |            5.4 |
| reupload_archive | AU     | Kekhawatiran umum AI      |              4.1 |              3.4 |            0.7 |
| reupload_archive | HC     | Hak cipta                 |              0.4 |              0.7 |           -0.3 |
| reupload_archive | LT     | Lainnya                   |              0   |              0   |            0   |

Chi-square: third_party: {'chi2': 128.21, 'dof': 6, 'p': 3.06e-25, 'cramers_v': 0.361, 'n': 982, 'note': 'LT excluded (3 comments); comments are clustered in 7 cases, so p-values overstate certainty and are descriptive only'}; reupload_archive: {'chi2': 17.76, 'dof': 6, 'p': 0.00685, 'cramers_v': 0.166, 'n': 642, 'note': 'LT excluded (3 comments); comments are clustered in 7 cases, so p-values overstate certainty and are descriptive only'}

## Per kasus (% kolom)

| case_id   | org_type   | video_type       | verifikasi          |   n |   KV |   KO |   PK |   AK |   EJ |   AU |   HC |   LT |
|:----------|:-----------|:-----------------|:--------------------|----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| C01       | commercial | third_party      | credible_media      | 276 | 26.4 | 10.5 | 14.5 | 12   | 12   | 11.6 | 12   |  1.1 |
| C02       | government | third_party      | credible_media      |  65 | 32.3 | 16.9 | 35.4 | 15.4 |  0   |  0   |  0   |  0   |
| C03       | government | reupload_archive | to_verify           | 493 | 37.5 | 16.6 | 17   |  7.5 | 16.8 |  4.1 |  0.4 |  0   |
| C04       | government | third_party      | credible_media      | 187 | 24.6 | 39.6 |  5.3 | 23   |  3.2 |  4.3 |  0   |  0   |
| C05       | commercial | reupload_archive | to_verify           |  77 | 55.8 | 13   |  9.1 |  3.9 | 14.3 |  3.9 |  0   |  0   |
| C06       | commercial | reupload_archive | to_verify           |  72 | 55.6 | 16.7 |  8.3 |  6.9 |  8.3 |  2.8 |  1.4 |  0   |
| C07       | government | third_party      | official_disclosure | 457 | 12.9 | 30.2 | 22.5 | 19.9 |  3.7 |  7.7 |  3.1 |  0   |

## Ko-okurensi (tema utama x tema kedua)

| tema_utama   |   KV |   KO |   PK |   AK |   AU |   HC |
|:-------------|-----:|-----:|-----:|-----:|-----:|-----:|
| KV           |    0 |   15 |    9 |    4 |    1 |    1 |
| KO           |    7 |    0 |    5 |   14 |    1 |    0 |
| PK           |   11 |    9 |    0 |   15 |    2 |    4 |
| AK           |    6 |    4 |   36 |    0 |    0 |    0 |
| AU           |    0 |    0 |    2 |    0 |    0 |    0 |
| HC           |    3 |    0 |    2 |    1 |    0 |    0 |

Pasangan tersering (tanpa urutan): AK+PK 51, KO+KV 22, KV+PK 20, AK+KO 18, KO+PK 14, AK+KV 10, HC+PK 6, HC+KV 4

## Robustness: hanya kasus terverifikasi (credible_media, official_disclosure; pemerintah C02, C04, C07, komersial C01; n=985)

| kode   | tema                      |   pct_government |   pct_commercial |   selisih_poin |   pct_government_semua |   pct_commercial_semua |   selisih_poin_semua |
|:-------|:--------------------------|-----------------:|-----------------:|---------------:|-----------------------:|-----------------------:|---------------------:|
| KV     | Kualitas visual           |             17.8 |             26.4 |           -8.6 |                   25.9 |                   36.7 |                -10.8 |
| KO     | Kepantasan organisasi     |             31.5 |             10.5 |           21   |                   25.4 |                   12   |                 13.4 |
| PK     | Pekerja kreatif           |             19.2 |             14.5 |            4.7 |                   18.3 |                   12.5 |                  5.8 |
| AK     | Biaya, anggaran & korupsi |             20.3 |             12   |            8.3 |                   15.1 |                    9.6 |                  5.5 |
| EJ     | Ejekan tanpa alasan       |              3.2 |             12   |           -8.8 |                    8.8 |                   11.8 |                 -3   |
| AU     | Kekhawatiran umum AI      |              6.1 |             11.6 |           -5.5 |                    5.2 |                    8.7 |                 -3.5 |
| HC     | Hak cipta                 |              2   |             12   |          -10   |                    1.3 |                    8   |                 -6.7 |
| LT     | Lainnya                   |              0   |              1.1 |           -1.1 |                    0   |                    0.7 |                 -0.7 |

Pada subset ini sisi komersial hanya diwakili 1 kasus, sehingga perbedaan jenis organisasi dan perbedaan kasus tidak bisa dipisahkan sepenuhnya. Semua kasus terverifikasi berjenis video third_party, jadi RQ3 tidak bisa diuji ulang pada subset ini.

Chi-square: {'chi2': 128.21, 'dof': 6, 'p': 3.06e-25, 'cramers_v': 0.361, 'n': 982, 'note': 'LT excluded (3 comments); comments are clustered in 7 cases, so p-values overstate certainty and are descriptive only'}
