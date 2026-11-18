# Anamedsos-tk: Struktur Keberatan terhadap GenAI dalam Komentar YouTube

Kode tugas kelompok CSIE604284 Analitika Media Sosial (TK-2 pengumpulan data, TK-3 analisis data): *Analisis Struktur Keberatan dalam Komentar Berbahasa Indonesia terhadap Penggunaan Generative AI dalam Komunikasi Visual Institusional dan Komersial di YouTube*.

Pipeline mengambil komentar dan balasan YouTube dari video yang dikurasi manual, menyamarkan identitas penulis, memeriksa kualitas data, menyiapkan teks untuk BERTopic, memberi label relevansi, sikap, dan tema keberatan, lalu membuat tabel dan grafik untuk tiga pertanyaan penelitian:

- **RQ1** tema keberatan apa yang muncul dalam komentar yang menolak penggunaan GenAI;
- **RQ2** bagaimana komposisi tema berbeda antara kasus pemerintah dan komersial;
- **RQ3** bagaimana komposisi tema berbeda antara video pihak ketiga dan unggahan ulang/arsip.

Desain deskriptif-komparatif dan eksploratif: tidak ada klaim kausal, dan korpus tidak mewakili seluruh masyarakat Indonesia.

## Struktur repositori

| Folder | Isi |
|---|---|
| `config/` | `videos_manifest.csv` (daftar video, kasus, jenis organisasi/video, status verifikasi) dan `quality_overrides.csv` (keputusan manual reviewer) |
| `src/` | Skrip pipeline utama, dijalankan berurutan (lihat di bawah) |
| `resources/` | Kamus slang (Salsabila dkk., 2018), koreksi slang, dan daftar stopword |
| `data/<YYYYMMDD>/` | Hasil pengambilan: `raw/` (JSON respons API), `comments.csv`, `videos.csv`, `collection_log.json` |
| `data/interim/` | Hasil pemeriksaan kualitas (flag, tidak ada baris yang dihapus) |
| `data/processed/` | Teks siap BERTopic, embedding cache, label relevansi, sentimen |
| `experiments/` | Run BERTopic (`runs.csv`), pelabelan relevansi/sikap/tema, validasi, adjudikasi, statistik deskriptif, evaluasi sentimen |
| `docs/` | Proposal, materi kuliah, codebook, panduan penulisan, tabel dan grafik hasil |
| `archive/` | Skrip pilot lama (tidak dipakai di pipeline akhir) |

## Persiapan

Membutuhkan Python 3.11 atau lebih baru (hasil yang dilaporkan dibuat dengan Python 3.12.5 dan versi library di `requirements.txt`). Semua perintah dijalankan dari **root repositori**, karena path di skrip relatif terhadap root.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp key.env.example key.env       # lalu isi YOUTUBE_API_KEY dan AUTHOR_HASH_SALT
```

API key dibuat di Google Cloud Console dengan mengaktifkan **YouTube Data API v3**. `key.env` dikecualikan dari git dan tidak boleh di-commit. Model yang diunduh otomatis dari Hugging Face: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (embedding), `w11wo/indonesian-roberta-base-sentiment-classifier` dan `cardiffnlp/twitter-xlm-roberta-base-sentiment` (sentimen).

## Menjalankan pipeline

Data 30 September 2026 sudah ada di `data/20260930/`, jadi langkah 1 tidak perlu diulang untuk mereproduksi hasil.

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

### 4. BERTopic, relevansi, dan sentimen

```bash
python src/topics_pass1.py --grid
python src/topics_pass1.py --final --n-neighbors 15 --min-cluster-size 15 --variant a
python src/reduce_outliers_pass1.py --run pass1_v1_nn15_mcs15_a
python src/build_relevance.py --check       # menyusun label relevansi dari label topik + label per komentar
python src/sentiment_relevant.py --version v1
python src/topics_pass2.py --grid
python src/topics_pass2.py --final --n-neighbors 30 --min-cluster-size 10 --variant a
```

Setiap run BERTopic dicatat di `experiments/runs.csv` (seed 42). Embedding di-cache di `data/processed/embeddings_mpnet_v1.npy` dan hanya dihitung ulang jika teks berubah (sekitar 4 menit di CPU). `build_relevance.py --check` membandingkan hasil susunan ulang dengan berkas yang ada; tanpa `--check` (dengan `--overwrite`) berkas ditulis ulang.

### 5. Tabel, grafik, dan evaluasi (TK-3)

```bash
python experiments/themes_v1/tabel_grafik_v2.py   # RQ1-RQ3, per kasus, robustness, kookurensi (fig1-fig5)
python src/descriptive_stats.py                   # statistik deskriptif: kasus, pengguna, waktu, like, kata khas (fig6-fig7)
python src/sentiment_eval.py                      # sentimen vs label sikap manusia: P/R/F1, confusion matrix (fig8)
python experiments/auto_check_v1/auto_check.py    # opsional: cek konsistensi label dengan classifier embedding
```

Ketiga skrip pertama hanya membaca berkas yang sudah ada dan selesai dalam hitungan detik. Output: `experiments/themes_v1/hasil_v2/`, `experiments/descriptive_v1/`, `experiments/sentiment_eval_v1/`; salinan gambar dan tabel untuk penulisan ada di `docs/paket_penulisan_hasil/`.

## Parameter penting

| Komponen | Nilai |
|---|---|
| Seed | UMAP `random_state=42`; sampel validasi `seed=42`; pilot codebook `seed=7` |
| Embedding | `paraphrase-multilingual-mpnet-base-v2`, maks. 128 token |
| UMAP | `n_components=5`, `min_dist=0`, cosine; `n_neighbors` 15 (putaran 1) / 30 (putaran 2) |
| HDBSCAN | `min_cluster_size` 15 / 10, `min_samples=5`, `eom` |
| Vectorizer | `ngram_range=(1,2)`, `min_df=2`, stopword `resources/stopwords_bertopic_v1.txt`, `reduce_frequent_words=True` |
| Reduksi outlier | kemiripan kosinus ke centroid topik 768-d, ambang 0,555 (persentil 5) |
| Sentimen | `max_length=256`, teks `text_embed` |
| Kata khas per kelompok | weighted log-odds dengan prior Dirichlet informatif (Monroe dkk., 2008), kata dengan frekuensi ≥ 5 |
| Uji perbandingan | chi-square + Cramér's V, deskriptif saja (komentar berkelompok dalam 7 kasus); interval Wilson 95% |

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
| Menolak penggunaan GenAI (dikode tema) | 1.627 |

Tema utama keberatan: kualitas visual 28,7%, kepantasan organisasi 21,9%, pekerja kreatif 16,8%, biaya/anggaran/korupsi 13,6%, ejekan tanpa alasan 9,6%, kekhawatiran umum AI 6,1%, hak cipta 3,1%.

## Etika dan data

Data berasal dari komentar publik YouTube. Penyimpanan bersifat **pseudonim**, bukan anonim: teks dan ID komentar masih memungkinkan penelusuran ulang. Gunakan data hanya untuk keperluan penelitian ini, jangan kutip komentar secara langsung dalam publikasi, dan patuhi [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).
