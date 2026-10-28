# Anamedsos-tk: Data Collection Pipeline

Kode tugas kelompok CSIE604284 Analitika Media Sosial (TK-2): *Analisis Struktur Keberatan dalam Komentar Berbahasa Indonesia terhadap Penggunaan Generative AI dalam Komunikasi Visual Institusional dan Komersial di YouTube*.

Pipeline mengambil komentar dan balasan YouTube dari video yang dikurasi manual, menyamarkan identitas penulis, memeriksa kualitas data, lalu menyiapkan teks untuk BERTopic dan pelabelan.

## Struktur repositori

| Folder | Isi |
|---|---|
| `config/` | `videos_manifest.csv` (daftar video, kasus, jenis organisasi/video) dan `quality_overrides.csv` (keputusan manual reviewer) |
| `src/` | Skrip pipeline utama, dijalankan berurutan (lihat di bawah) |
| `resources/` | Kamus slang, koreksi slang, dan daftar stopword |
| `data/<YYYYMMDD>/` | Hasil pengambilan: `raw/` (JSON respons API), `comments.csv`, `videos.csv`, `collection_log.json` |
| `data/interim/` | Hasil pemeriksaan kualitas |
| `data/processed/` | Teks siap BERTopic, label relevansi, sentimen, embedding |
| `experiments/` | Run BERTopic (`runs.csv`), pelabelan relevansi/sikap/tema, validasi, dan adjudikasi |
| `docs/` | Proposal TK-1, materi kuliah, codebook, tabel dan grafik hasil |
| `archive/` | Skrip pilot lama (tidak dipakai di pipeline akhir) |

## Persiapan

Membutuhkan Python 3.11 atau lebih baru. Semua perintah dijalankan dari **root repositori**, karena path di skrip relatif terhadap root.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp key.env.example key.env       # lalu isi YOUTUBE_API_KEY dan AUTHOR_HASH_SALT
```

API key dibuat di Google Cloud Console dengan mengaktifkan **YouTube Data API v3**. `key.env` dikecualikan dari git dan tidak boleh di-commit.

## Menjalankan pipeline

### 1. Pengambilan komentar (`src/fetch_comments.py`)

```bash
python src/fetch_comments.py --dry-run      # validasi manifest tanpa request API
python src/fetch_comments.py                # ambil semua video dengan include=yes
python src/fetch_comments.py --only ID1 ID2 # ambil video tertentu saja
```

- Endpoint: `videos.list` (`snippet,statistics`), `commentThreads.list` (`snippet,replies`), dan `comments.list` (`snippet`, per `parentId`) untuk utas yang balasannya terpotong.
- Pagination mengikuti `nextPageToken` sampai habis, dengan `maxResults=100` dan `textFormat=plainText`.
- Setiap request memiliki timeout 30 detik. Error jaringan dan HTTP 500/502/503/504 dicoba ulang hingga 4 kali (jeda 2, 4, 8 detik). `quotaExceeded` menghentikan run.
- Utas yang muncul dua kali (misalnya komentar yang di-pin) hanya disimpan sekali.
- Pseudonimisasi dilakukan sebelum disimpan: `authorChannelId` diganti HMAC-SHA256 (16 heksadesimal pertama), nama/foto/URL kanal dihapus, dan `@handle` di teks diganti `@user`.
- Output ditulis ke `data/<tanggal UTC>/`. Run tidak menimpa hasil yang sudah ada kecuali dengan `--overwrite`.
- Setiap endpoint list berbiaya 1 unit kuota per request. Run 30 September 2026 memakai sekitar 67 request (8 video, 28 halaman utas, 38 halaman balasan), jauh di bawah kuota harian default 10.000 unit.

### 2. Pemeriksaan kualitas (`src/quality_check.py`)

```bash
python src/quality_check.py --raw-dir data/20260930 --version v1
```

Validasi record dan dataset, lalu memberi flag (pemilik kanal, tanpa isi, spam, pengulangan penulis sama, bukan bahasa Indonesia via Lingua) dan menetapkan kolom `eligible`. Komentar tidak dihapus, hanya ditandai. Output: `data/interim/comments_quality_v1.csv` dan `quality_report_v1.md`.

### 3. Prapemrosesan (`src/preprocess_bertopic.py`)

```bash
python src/preprocess_bertopic.py
```

Menghasilkan `text_embed` (pembersihan minimal untuk embedding) serta `text_repr_a` dan `text_repr_b` (representasi kata penciri topik, B dengan normalisasi slang). Stopword disimpan terpisah untuk `CountVectorizer`. Output: `data/processed/comments_bertopic_v1.csv`.

### 4. Analisis lanjutan

```bash
python src/topics_pass1.py --grid
python src/topics_pass1.py --final --n-neighbors 15 --min-cluster-size 15 --variant a
python src/reduce_outliers_pass1.py --run pass1_v1_nn15_mcs15_a
python src/sentiment_relevant.py --version v1
python src/topics_pass2.py --final --n-neighbors 30 --min-cluster-size 10 --variant a
```

Setiap run BERTopic dicatat di `experiments/runs.csv` (seed 42).

## Pelabelan relevansi, sikap, dan tema

Pelabelan per komentar dilakukan oleh model bahasa **Claude (Anthropic)** mengikuti panduan tertulis (`experiments/stance_v1/panduan_sikap.md`, `experiments/themes_v1/codebook_tema.md`). Langkah ini tidak bisa dijalankan ulang dari skrip. Pada setiap tahap, anggota tim mengode 100 komentar acak tanpa melihat label Claude, lalu perbedaan diputuskan lewat adjudikasi. Label final dan sumbernya tersimpan per `commentId`:

| Tahap | Berkas label final | Cohen's κ buta (manusia vs Claude) |
|---|---|---|
| Relevansi | `data/processed/comments_relevance_v1.csv` | 0,267 (n=100) |
| Sikap | `experiments/stance_v1/sikap_final_v2.csv` | 0,235 (n=99) |
| Tema | `experiments/themes_v1/tema_final_v2.csv` | 0,452 (n=100) |

Skrip di `experiments/*/` menyiapkan berkas validasi, menerapkan revisi panduan (v2), dan membuat tabel serta grafik di `docs/paket_penulisan_hasil/`.

## Ringkasan hasil

| Tahap | Jumlah komentar |
|---|---|
| Korpus unik (8 video, 7 kasus) | 3.307 |
| Lolos pemeriksaan kualitas | 3.145 |
| Relevan | 2.288 |
| Menolak penggunaan GenAI | 1.627 |

## Etika dan data

Data berasal dari komentar publik YouTube. Penyimpanan bersifat **pseudonim**, bukan anonim: teks dan ID komentar masih memungkinkan penelusuran ulang. Gunakan data hanya untuk keperluan penelitian ini, jangan kutip komentar secara langsung dalam publikasi, dan patuhi [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).
