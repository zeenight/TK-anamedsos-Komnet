# Panduan Penulisan: Metodologi Lanjutan dan Bab Hasil

Dokumen ini untuk anggota tim yang menulis bagian analisis di Bab 2 dan seluruh Bab 3 (Hasil). Ini lanjutan dari `docs/panduan_penulisan_bab2.md`, yang hanya mencakup tahap sampai BERTopic putaran 1.

Status per 24 Oktober 2026. Semua tahap analisis sudah selesai.

**Isi paket ini:**

| Folder/file | Isi |
|---|---|
| `panduan_penulisan_hasil.md` | Dokumen ini |
| `gambar/fig1`–`fig5` | Lima grafik siap pakai (PNG, 300 dpi) |
| `tabel/tabel_final.md` | Semua tabel hasil dalam Markdown, bisa disalin ke Word/LaTeX |
| `tabel/*.csv` | Tabel yang sama dalam CSV, kalau perlu diformat ulang |
| `tabel/uji_chi2.json` | Hasil uji chi-square dan Cramér's V |
| `codebook_tema.md` | Codebook tema v2: definisi, contoh, aturan kasus sulit |

**Aturan umum:** sama dengan panduan Bab 2. Pakai kala lampau, tulis angka yang bisa ditelusuri ke file di paket ini, gunakan istilah yang konsisten (bagian 5), lalu jalankan /humanizer setelah draft selesai.

> **Penting: jangan menulis klaim kausal.** Semua perbandingan bersifat deskriptif. Tulis "komentar pada kasus pemerintah lebih sering…", jangan "karena pemerintah, warganet…".

---

## 1. Alur lengkap dan angka corong

Bab 2 sebaiknya punya satu diagram alur atau satu tabel corong yang memperlihatkan jumlah komentar di setiap tahap.

| Tahap | Komentar | Keterangan |
|---|---|---|
| Dikumpulkan | 3.307 | 8 video, 7 kasus, 30 September 2026 |
| Lolos pemeriksaan kualitas | 3.145 | tanpa komentar pemilik kanal, spam, duplikat, non-Indonesia |
| Relevan dengan penggunaan GenAI | 2.288 (72,8%) | BERTopic putaran 1 ditambah pelabelan per komentar |
| Sikap: menolak (`tolak`) | 1.627 (71,1% dari yang relevan) | lain 510, mendukung 151 |
| Dikode tema | 1.627 | codebook v2, satu tema utama per komentar |

---

## 2. Bab 2: sub-bab analisis yang perlu ditambahkan

Panduan Bab 2 berhenti di 2.7.1 (BERTopic putaran 1). Ganti kerangka 2.7.2 di sana dengan sub-bab berikut.

### 2.7.2 Penentuan komentar relevan

**Poin wajib:**
- Hasil BERTopic putaran 1: 44 topik. Topik diberi label **relevan / tidak relevan / campuran** oleh dua anggota tim (κ = 0,20 pada 8 topik yang tumpang tindih; ketidaksepakatan diputuskan oleh satu anggota).
- Outlier (topik −1) dialokasikan ulang ke topik terdekat dengan kemiripan kosinus terhadap centroid topik, memakai ambang 0,555 (persentil ke-5 kemiripan anggota topik terhadap topiknya sendiri).
- Komentar di topik campuran (1.147 komentar) dilabeli satu per satu dengan membaca konteks: judul video dan komentar induk.
- Prinsip yang dipakai: **relevansi dinilai dari konteks, bukan kata kunci.** Komentar tanpa kata "AI" tetap relevan kalau, dalam konteks videonya, jelas menanggapi penggunaan GenAI.
- Hasil: 2.288 dari 3.145 komentar relevan (72,8%).

### 2.7.3 Penentuan sikap: mengapa bukan analisis sentimen

**Poin wajib:**
- Dua model sentimen dijalankan sebagai alat bantu: `w11wo/indonesian-roberta-base-sentiment-classifier` dan `cardiffnlp/twitter-xlm-roberta-base-sentiment`. Kesepakatan antarmodel 0,687.
- Saat dibaca, model salah membaca sarkasme ("Kreatif sekali", "Salut! Pemerintah berhasil…" dibaca positif) dan keberatan yang jelas ("Jelek bat asli 🤣" dibaca netral).
- Hanya 941 dari 1.290 komentar yang dinilai negatif oleh kedua model ternyata benar-benar menolak; 39% komentar yang menolak tidak terdeteksi negatif oleh kedua model. **Nada tidak sama dengan sikap.** Karena itu, pemilihan komentar keberatan memakai label **sikap** (`tolak` / `dukung` / `lain`), bukan sentimen.
- Sikap dilabeli dengan panduan tertulis (21 aturan kasus sulit), lalu divalidasi (lihat 2.8).

### 2.7.4 BERTopic putaran 2 dan penyusunan codebook

**Poin wajib:**
- BERTopic dijalankan ulang pada 1.627 komentar `tolak`, dengan embedding yang sama (`paraphrase-multilingual-mpnet-base-v2`). Ada 24 konfigurasi yang dicoba (n_neighbors 10/15/30 × min_cluster_size 8/10/15/20 × dua versi teks). Yang dipilih nn30 / mcs10: 25 topik, 26,3% outlier, topik terbesar 10,6%, c_v 0,399. Alasan memilihnya: tidak ada satu klaster besar yang menampung semua.
- **Topik BERTopic bukan hasil akhir.** Topik dipakai sebagai bahan untuk menyusun kategori tema, lalu tema dikode manual per komentar. Alasannya: beberapa topik mencampur alasan yang berbeda, dan balasan pendek mengelompok berdasarkan bentuk kalimat, bukan isinya.
- Codebook disusun dari topik BERTopic dan tema yang diharapkan proposal, diuji pada 50 komentar pilot, lalu direvisi tiga kali (v0 → v1 → v2). Hasil akhirnya **tujuh tema** (lihat bagian 3.1) dengan 27 aturan kasus sulit.
- Setiap komentar diberi satu **tema utama** (alasan yang paling ditekankan) dan, kalau ada, satu **tema kedua**. Proporsi dihitung dari tema utama, sehingga totalnya selalu 100%.

### 2.8 Peran AI dan reliabilitas pelabelan (WAJIB ditulis terbuka)

Pelabelan relevansi per komentar, sikap, dan tema untuk seluruh korpus dilakukan oleh **Claude (model bahasa Anthropic)** di dalam sesi kerja, mengikuti panduan tertulis. Pada setiap tahap, anggota tim mengode sampel acak secara **buta** (tanpa melihat label Claude), lalu ketidaksepakatan diputuskan oleh anggota tim (adjudikasi). Panduan direvisi dari hasil adjudikasi, dan label di luar sampel diperbarui mengikuti aturan baru.

Laporkan tabel ini apa adanya:

| Tahap | Sampel | κ buta (manusia vs Claude) | Setelah adjudikasi: Claude vs final |
|---|---|---|---|
| Relevansi per komentar | 100 | 0,267 | 0,71 |
| Sikap | 99 | 0,235 | 0,757 |
| Tema (kalibrasi pilot, codebook v0) | 49 | 0,484 | – |
| Tema (validasi, codebook v1.1) | 100 | **0,452** | 0,753 (validator vs final: 0,65) |

**Cara menulisnya:**
- Angka reliabilitas yang dilaporkan adalah **κ buta**, bukan κ setelah adjudikasi. κ setelah adjudikasi tinggi sebagian karena keputusan adjudikasi dipakai untuk merevisi panduan.
- Semua κ buta di bawah ambang yang umum dipakai (0,6). Jelaskan sumber utamanya: perbedaan ambang batas, bukan salah baca. Pada tema, validator memakai kode "kekhawatiran umum AI" 22 kali, sedangkan Claude 3 kali; tanpa baris itu κ menjadi 0,588.
- Tulis bahwa label versi akhir (relabel setelah adjudikasi) **tidak** divalidasi ulang dengan sampel buta baru.

**Contoh kalimat:**
> Pengodean seluruh korpus dilakukan dengan bantuan model bahasa (Claude) yang mengikuti codebook tertulis. Untuk menguji konsistensinya, 100 komentar acak dikode ulang oleh anggota tim tanpa melihat kode model. Kesepakatan tema utama mencapai 55%, dengan κ Cohen sebesar 0,452…

### 2.9 Analisis perbandingan

- RQ1: proporsi tema utama pada seluruh komentar `tolak`, dengan interval kepercayaan Wilson 95%.
- RQ2 dan RQ3: proporsi tema utama di setiap kelompok. Perbandingan memakai **proporsi, bukan jumlah**, karena korpus tidak seimbang (pemerintah 1.202 vs komersial 425 komentar `tolak`).
- Chi-square dan Cramér's V dilaporkan sebagai **ukuran deskriptif**. Komentar mengelompok di dalam 7 kasus (tidak independen), sehingga nilai p terlalu optimistis.
- Karena jenis organisasi dan jenis video tumpang tindih, RQ2 juga dibandingkan **di dalam** setiap jenis video. Hasil per kasus juga dilaporkan.
- **Robustness check:** perbandingan RQ2 diulang hanya dengan kasus yang terverifikasi: lewat berita media kredibel (C01, C02, C04) atau lewat pengakuan resmi organisasi bahwa animasinya dibuat dengan AI (C07, keterangan di akhir video yang diunggah di Instagram Menteri Komdigi). Tulis jenis bukti per kasus di tabel kasus.

---

## 3. Bab 3: Hasil

Struktur yang disarankan: 3.1 tema keberatan (RQ1), 3.2 pemerintah vs komersial (RQ2), 3.3 jenis video (RQ3), 3.4 variasi antarkasus dan robustness, 3.5 tema yang muncul bersamaan.

### 3.1 RQ1: tema keberatan → **Gambar 1** (`fig1_rq1_tema.png`)

| Kode | Tema | % | Contoh komentar (dari codebook) |
|---|---|---|---|
| KV | Kualitas visual | 28,7 | "menit ke 🤣🤣 tangan nyatu kanan kiri" · "Mengerikan" · "Masih bagusan animasi minecraft indo 💀💀" |
| KO | Kepantasan organisasi | 21,9 | "Pke ai bukan inovasi tp kemunduran" · "Damkar mah gak usah buat vidio ai segala udh terpercaya di masyarakat" |
| PK | Pekerja kreatif | 16,8 | "Mengapa iklan pemerintah harus pakai ai padahal ada animator lokal😂" · "Kami dari SKDK liat animasi kaya gini rada sakit hati😂" |
| AK | Biaya, anggaran & korupsi | 13,6 | "pff anggaran tinggi hasilnya ai🖐️😂🖐️" · "Hemat anggaran / Korupsi anggaran?" |
| EJ | Ejekan tanpa alasan | 9,6 | "sangat layak dihujat" · "Ai pula😂" |
| AU | Kekhawatiran umum tentang AI | 6,1 | "Kaya seolah olah ada entitas lain nya mengganti kan manusia serem" · "Axe ID juga iklannya pake AI" |
| HC | Hak cipta | 3,1 | "AI itu cuma nyomot hasil karya orang lain tanpa ngasih royalti ke kreator" |
| LT | Lainnya | 0,2 | (3 komentar) |

**Pesan utama:** keberatan bukan satu kategori "anti-AI". Empat tema terbesar (kualitas, kepantasan organisasi, pekerja kreatif, uang) masing-masing mencakup lebih dari 13%. Hanya 9,6% komentar yang menolak tanpa alasan apa pun. Tema yang diharapkan proposal semuanya muncul, ditambah dua tema baru: **biaya/anggaran/korupsi** dan **kekhawatiran umum tentang AI**. Hak cipta, yang ada di proposal, ternyata kecil (3,1%) dan hampir seluruhnya berasal dari satu kasus (C01).

**Kutipan:** jangan kutip komentar verbatim di laporan (TK2 §3.6: hanya agregat). Pakai parafrase singkat tanpa identitas akun; contoh di bawah hanya untuk tim.

### 3.2 RQ2: pemerintah vs komersial → **Gambar 2** (`fig2_rq2_org_type.png`)

| Tema | Pemerintah (n=1.202) | Komersial (n=425) | Selisih (poin) |
|---|---|---|---|
| Kualitas visual | 25,9 | 36,7 | −10,8 |
| Kepantasan organisasi | 25,4 | 12,0 | **+13,4** |
| Pekerja kreatif | 18,3 | 12,5 | +5,8 |
| Biaya, anggaran & korupsi | 15,1 | 9,6 | +5,5 |
| Ejekan tanpa alasan | 8,8 | 11,8 | −3,0 |
| Kekhawatiran umum AI | 5,2 | 8,7 | −3,5 |
| Hak cipta | 1,3 | 8,0 | −6,7 |

χ² = 106,4; df = 6; Cramér's V = 0,256 (deskriptif).

**Pesan utama:** pada kasus pemerintah, keberatan lebih banyak menyasar **organisasinya**: apakah pantas lembaga pemerintah memakai GenAI, dan ke mana uangnya. Pada kasus komersial, keberatan lebih banyak menyasar **hasilnya**: kualitas visual dan hak cipta.

**Wajib ditulis bersama hasil ini (lihat 3.4):**
- Di dalam video pihak ketiga, selisih kepantasan organisasi justru **lebih besar** (pemerintah 31,5% vs komersial 10,5%), begitu pula anggaran (20,3% vs 12,0%). Pola "pemerintah → kepantasan dan uang" bertahan.
- Selisih kualitas visual sebagian besar berasal dari dua kasus komersial di video re-upload (C05, C06; 56% kualitas visual). Tanpa keduanya (robustness check), selisihnya mengecil dan tidak konsisten antarkasus pemerintah.

### 3.3 RQ3: jenis video → **Gambar 3** (`fig3_rq3_video_type.png`)

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

**Pesan utama:** di video re-upload yang hanya menampilkan iklannya, komentar lebih banyak bereaksi pada **tampilan** dan lebih sering berupa ejekan tanpa alasan. Di video pihak ketiga yang memberi ulasan atau *framing*, komentar lebih sering membawa **argumen**: kepantasan organisasi, anggaran, hak cipta. Ini interpretasi yang masuk akal, tetapi tidak diuji; tulis sebagai dugaan ("kemungkinan karena…").

**Wajib disebut:** korpus tidak berisi video unggahan resmi, sehingga RQ3 hanya membandingkan dua dari tiga jenis video yang direncanakan di proposal.

### 3.4 Variasi antarkasus dan robustness → **Gambar 4** (`fig4_per_kasus.png`)

Gambar 4 adalah peta panas tema × kasus. Setiap kolom berjumlah 100%. Temuan yang perlu disebut:
- **C05 dan C06** (filler Ramadan RTV dan adzan Mentari TV): 56% kualitas visual. Banyak komentar soal wajah dan gerak yang menyeramkan.
- **C04** (iklan POLRI): 40% kepantasan organisasi, 23% anggaran.
- **C02** (video MBG Komdigi): 35% pekerja kreatif. Komentar membandingkannya dengan animasi BNI yang dibuat manusia.
- **C07** (animasi AI Komdigi kedua): 30% kepantasan organisasi. Banyak komentar soal "lomba AI" dan pemakaian AI yang berulang.
- **C01** (Indomie): satu-satunya kasus dengan hak cipta yang besar (12%) dan kekhawatiran umum AI (12%), karena kolom komentarnya berisi debat AI art.

**Status verifikasi kasus** (dasar subset robustness; tingkat verifikasi mengikuti proposal):

| Kasus | Status | Bukti |
|---|---|---|
| C01 Indomie | Media kredibel | Suara.com (2023) [11] |
| C02 MBG Komdigi | Media kredibel | Tempo [9], [10] |
| C04 POLRI "Pahlawan Masa Kini" | Media kredibel | Suara.com, 23 Juni 2025: video dirilis Divisi Humas Polri di akun X resmi pada 22 Juni 2025 [ISI nomor referensi] |
| C07 Animasi AI Komdigi (Maret 2025) | Pernyataan resmi | Diunggah di Instagram Menteri Komdigi Meutya Hafid; keterangan di akhir video menyatakan animasi dibuat dengan AI [ISI link/tanggal unggahan] |
| C03, C05, C06 | Belum terverifikasi | Hanya dari isi video dan komentar |

**Robustness check** (`tabel_robustness.csv`): hanya 4 kasus terverifikasi, yaitu pemerintah C02, C04, C07 (n=709) vs komersial C01 (n=276); total 985 komentar `tolak`. χ² = 128,2; df = 6; Cramér's V = 0,361 (deskriptif).

| Tema | Pemerintah (terverifikasi) | Komersial (C01) | Selisih | Selisih di semua kasus |
|---|---|---|---|---|
| Kepantasan organisasi | 31,5 | 10,5 | **+21,0** | +13,4 |
| Biaya, anggaran & korupsi | 20,3 | 12,0 | +8,3 | +5,5 |
| Pekerja kreatif | 19,2 | 14,5 | +4,7 | +5,8 |
| Kualitas visual | 17,8 | 26,4 | −8,6 | −10,8 |
| Ejekan tanpa alasan | 3,2 | 12,0 | −8,8 | −3,0 |
| Kekhawatiran umum AI | 6,1 | 11,6 | −5,5 | −3,5 |
| Hak cipta | 2,0 | 12,0 | −10,0 | −6,7 |

- Semua arah selisih **sama** dengan hasil utama. Selisih kepantasan organisasi dan anggaran malah membesar.
- Konsistensi per kasus (lihat `tabel_per_kasus.csv`): kepantasan organisasi dan anggaran lebih tinggi daripada C01 di **ketiga** kasus pemerintah (KO 16,9 / 39,6 / 30,2 vs 10,5; AK 15,4 / 23,0 / 19,9 vs 12,0). Hak cipta, ejekan, dan kekhawatiran umum AI lebih rendah di ketiganya. Pekerja kreatif dan kualitas visual **tidak** konsisten: PK tinggi di C02 (35,4) tetapi rendah di C04 (5,3); KV tinggi di C02 (32,3) tetapi rendah di C07 (12,9). Jadi yang kuat dari RQ2 adalah pola "pemerintah → kepantasan organisasi dan uang", bukan "pemerintah → pekerja kreatif".
- Sisi komersial hanya diwakili satu kasus (C01), jadi perbedaan jenis organisasi dan perbedaan kasus tetap tidak bisa dipisahkan sepenuhnya. Tulis ini secara eksplisit.
- Keempat kasus terverifikasi berjenis video pihak ketiga, sehingga subset ini sama dengan stratifikasi "di dalam video pihak ketiga" di 3.2, dan RQ3 tidak bisa diuji ulang di subset ini.

**Kalimat kunci untuk bagian ini:**
> Perbedaan antarkasus sama besarnya dengan perbedaan antarjenis organisasi, sehingga perbandingan RQ2 dan RQ3 perlu dibaca bersama hasil per kasus.

### 3.5 Tema yang muncul bersamaan → **Gambar 5** (`fig5_kookurensi.png`)

- 152 komentar (9,3%) menyebut dua alasan.
- Pasangan tersering adalah **biaya/anggaran + pekerja kreatif** (51 komentar), misalnya keluhan bahwa lembaga mampu membeli robot tetapi tidak mampu menyewa animator. Pasangan berikutnya: kualitas visual + kepantasan organisasi (22), kualitas visual + pekerja kreatif (20), anggaran + kepantasan organisasi (18).
- **Makna:** argumen soal uang sering dipakai untuk membela pekerja kreatif. Tema-tema ini saling terkait, tidak terpisah.

---

## 4. Keterbatasan yang wajib ditulis (Bab Penutup atau akhir Bab Hasil)

1. **Reliabilitas pelabelan:** semua κ buta di bawah 0,6 (relevansi 0,267; sikap 0,235; tema 0,452). Label akhir adalah hasil Claude yang direvisi setelah adjudikasi manusia, dan tidak divalidasi ulang dengan sampel buta baru.
2. **Peran model bahasa:** sebagian besar label dibuat oleh Claude. Validasi manusia hanya pada sampel 100 komentar per tahap, dan adjudikasi dilakukan oleh satu anggota tim.
3. **Efek kasus:** hanya 7 kasus (pemerintah 4, komersial 3). Perbedaan organisasi tidak bisa dipisahkan dari perbedaan kasus, dan uji statistik tidak memperhitungkan pengelompokan komentar dalam kasus.
4. **Tidak ada video unggahan resmi:** RQ3 hanya membandingkan pihak ketiga dan re-upload/arsip.
5. **Verifikasi kasus:** 3 dari 7 kasus (C03, C05, C06) masih berstatus `to_verify`; semuanya video re-upload/arsip. C07 diverifikasi lewat pengakuan resmi organisasi, bukan berita media. Robustness check menyisakan 4 kasus, dengan hanya satu kasus komersial.
6. **Ketidakseimbangan korpus:** komentar pemerintah sekitar tiga kali komentar komersial, dan Komdigi sendiri mencakup tiga kasus.
7. **Bahasa:** komentar berbahasa Inggris dikeluarkan, dan bahasa daerah tidak dideteksi terpisah.
8. **Representasi:** komentar YouTube tidak mewakili seluruh masyarakat Indonesia.

---

## 5. Istilah baku

| Pakai | Jangan |
|---|---|
| keberatan, komentar yang menolak (`tolak`) | komentar negatif (kecuali saat membahas sentimen) |
| tema utama, tema kedua | label, kategori (untuk tema) |
| kasus pemerintah / kasus komersial | iklan pemerintah (kalau maksudnya kelompok kasus) |
| video pihak ketiga, video re-upload/arsip | video reaksi, video mirror |
| kepantasan organisasi | etika organisasi |
| adjudikasi | voting, koreksi |
| κ buta | akurasi Claude |

Nama tema di teks dan grafik harus sama dengan tabel di 3.1.

---

## 6. Checklist sebelum draft dikirim

- [ ] Setiap gambar punya nomor, judul, dan rujukan di teks ("seperti terlihat pada Gambar 2…").
- [ ] Setiap angka cocok dengan `tabel/tabel_final.md`.
- [ ] Tidak ada klaim kausal atau klaim keterwakilan nasional.
- [ ] Peran Claude dan κ buta ditulis terbuka di 2.8.
- [ ] Hasil RQ2 selalu disertai catatan efek kasus (3.4).
- [ ] Tidak ada kutipan verbatim komentar (parafrase saja) dan tidak ada identitas akun.
- [ ] Sudah dicek dengan /humanizer.
