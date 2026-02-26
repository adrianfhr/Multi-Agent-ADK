# Evaluasi LLM (World 2 - Probabilistic)

Direktori ini berisi lapisan evaluasi aplikasi LLM dan Agent kita menggunakan [Ragas](https://docs.ragas.io/).

## Tujuan
Berbeda dengan Unit Tests (`tests/`) yang bersifat **deterministik** (benar/salah) dan cepat (milidetik), evaluasi LLM bersifat **probabilistik**. Jawaban yang dihasilkan oleh agen AI bisa bervariasi meski pertanyaannya sama, sehingga kita membutuhkan pendekatan lain (Metric-Driven Development) menggunakan *LLM-as-a-judge*.

## Komponen
1. **`golden_dataset.json`**: Dataset kunci jawaban berisi `question` dan panduan `ground_truth`. Dataset ini merupakan "benchmark" performa aplikasi.
2. **`eval_smart_info.py`**: Skrip yang memuat dataset, memanggil sub-agent Google ADK, dan menghasilkan metrik kualitas (Faithfulness, Answer Relevancy).

## Cara Menjalankan

Karena evaluasi ini menggunakan *LLM-as-a-judge* (menghabiskan token asli & waktu yang lebih lama), ini **tidak boleh** dimasukkan ke dalam CI yang berjalan setiap ada pull request/commit. Sebaiknya dijalankan sebagai *nightly build* atau saat akan merilis versi baru.

```bash
# Pastikan API keys di .env sudah diset
# Ragas defaultnya memerlukan OPENAI_API_KEY untuk model evaluator
make eval
```
