# Arsitektur Pengujian AI & RAG: Membelah Dua Dunia

Dokumen ini menjelaskan konsep inti dari materi **"Knowledge Sharing: Membelah Dua Dunia"**. Konsep ini diadopsi secara nyata di proyek Smart Info Assistant yang ada di repositori ini.

## 1. Analogi Dapur Restoran Bintang 5

Bayangkan aplikasi AI (RAG / Agent kita) adalah sebuah Restoran.

### World 1: Infrastruktur Dapur (Unit & Integration Test)
*   **Aktivitas**: Mengecek kompor menyala, suhu kulkas stabil, alat bersih.
*   **Karakteristik**: Deterministik (100% Ya/Tidak). Cepat (milidetik). Murah.
*   **Tools**: `pytest`, Ruff (Linter modern), mocks, `testcontainers`.
*   **Kapan Dijalankan**: *Setiap koki memotong bawang.* (i.e. Setiap kali ada commit PR baru di Git).

### World 2: Kritikal Makanan (LLM Evaluation)
*   **Aktivitas**: Menyewa kritikus makanan (LLM-as-a-judge) untuk mencicipi resep baru.
*   **Karakteristik**: Probabilistik (Output bisa sedikit berbeda). Lambat (API Calls). Mahal (Membutuhkan token uang sungguhan).
*   **Tools**: Ragas, TruLens, LangSmith, Golden Datasets.
*   **Kapan Dijalankan**: *Hanya saat meluncurkan menu baru atau menu telah berubah.* (i.e. *Nightly builds* atau pra-rilis/pemasangan ke Production).

---

## 2. Kenapa HARUS Dipisah?

Jika kita mencampur pengujian LLM generation dengan CI reguler kita:
1.  **Tagihan (Cost) Membengkak**: Menjalankan evaluasi terhadap LLM setiap PR kecil akan menghabiskan *credits* API dengan cepat.
2.  **Developer Experience (DX) Menurun**: Pengembang menjadi malas melakukan push karena CI menjadi lambat dan flaky (gagal karena limit *rate* API, bukan karena *code bug*).
3.  **Metrik yang Salah Tempat**: Lulus *flake8* atau `assert response == 200` tidak menjamin jawaban Agent AI kita bebas dari "*Hallucination/Fake Facts*". 

Oleh karena itu, proyek ini memiliki:
- `.github/workflows/ci.yml`: Berbasis Pytest/Ruff. Sangat cepat.
- `.github/workflows/eval.yml`: Berbasis Ragas. Agendanya terjadwal harian/nightly.
