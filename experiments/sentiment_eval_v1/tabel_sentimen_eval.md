# Evaluasi sentimen pretrained terhadap label sikap manusia

Dibuat oleh `src/sentiment_eval.py` v1.0. Baseline selalu-tolak: akurasi 0.66.

| model | acuan | n | P (neg→tolak) | R | F1 | akurasi 3 kelas | macro-F1 | κ | F1 tolak | F1 lain | F1 dukung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| id | final | 100 | 0.75 | 0.818 | 0.783 | 0.65 | 0.471 | 0.27 | 0.783 | 0.439 | 0.19 |
| id | zillan_blind | 99 | 0.915 | 0.747 | 0.823 | 0.697 | 0.4 | 0.143 | 0.823 | 0.261 | 0.118 |
| xlmr | final | 100 | 0.783 | 0.712 | 0.746 | 0.61 | 0.44 | 0.238 | 0.746 | 0.441 | 0.133 |
| xlmr | zillan_blind | 99 | 0.949 | 0.644 | 0.767 | 0.626 | 0.398 | 0.156 | 0.767 | 0.244 | 0.182 |

## Tabulasi silang sentimen × sikap (2.288 komentar relevan; sikap = sikap_final_v2)

| model | sikap | negative | neutral | positive |
|---|---|---|---|---|
| id | tolak | 1319 | 122 | 186 |
| id | lain | 374 | 63 | 73 |
| id | dukung | 117 | 3 | 31 |
| xlmr | tolak | 1051 | 384 | 192 |
| xlmr | lain | 247 | 195 | 68 |
| xlmr | dukung | 92 | 31 | 28 |
