# Petunjuk Pengujian Deterministik (World 1) 🧪

Direktori `tests/` ini adalah representasi dari **"Dunia Pertama"** dalam arsitektur AI Testing Pipeline kita: **Pengujian Deterministik & Cepat**.

Di dunia ini, kita mengamankan lapisan *Software Engineering* tradisional dari aplikasi AI kita. Kita **tidak** menguji kualitas generasi teks dari LLM di sini (itu tugas World 2 di `/evaluations`).

## Filosofi Pengujian 💡

1. **Deterministik (100% Ya/Tidak):** Tes di sini harus selalu mengembalikan hasil yang pasti (Lulus/Gagal). Tidak ada ruang untuk "mungkin" atau "jawaban sedikit berbeda".
2. **Tanpa Biaya (Zero Token Cost):** Rangkaian tes ini **tidak boleh** memanggil API LLM (Google Gemini, OpenAI, dll) secara nyata.
3. **Secepat Kilat (< 5 Detik):** Karena dijalankan setiap kali *Developer* membuat commit/PR, kecepatan adalah kunci untuk *Developer Experience* (DX) yang baik.
4. **Terisolasi (Mocking):** Semua dependensi eksternal, termasuk pemanggilan API pihak ketiga (cuaca, kurs, dll) **wajib di-mock**.

---

## Struktur Direktori 📂

```text
tests/
├── conftest.py               # Fixtures global untuk Pytest (contoh: mock HTTP client)
├── unit/                     # Pengujian level komponen terkecil (Tools/Functions)
│   └── test_tools.py         # Memastikan Tool mem-parsing JSON API dengan benar
└── integration/              # Pengujian level sub-sistem (Agent Routing & Guardrails)
    └── test_agents.py        # Memastikan Root Agent mendelegasikan tugas/memblokir secara benar
```

---

## Cara Menjalankan Tes 🚀

Pastikan Anda sudah menginstall dependensi *development* (`pip install -e .[dev]`).

**1. Menjalankan Semua Tes:**
```bash
make test
# atau
pytest tests/ -v
```

**2. Menjalankan Unit Tests Saja:**
```bash
make test-unit
# atau
pytest tests/unit/ -v
```

**3. Menjalankan Integration Tests Saja:**
```bash
make test-integration
# atau
pytest tests/integration/ -v
```

---

## Panduan Membuat Tes Baru ✍️

Jika Anda menambahkan fitur, tool, atau sub-agent baru ke dalam proyek ini, ikuti panduan berikut untuk menulis tesnya.

### 1. Menambahkan Tool Baru (Unit Test)
Jika Anda menambahkan fungsi Python baru di `src/agents/tools/info_tools.py` (misal: `get_stock_price`), Anda wajib menambah tesnya di `tests/unit/test_tools.py`.

**Aturan Emas:** *JANGAN PERNAH melakukan request HTTP sungguhan di Unit Test.* Gunakan `mocker` (dari `pytest-mock`) untuk memalsukan respon dari API.

**Contoh Template:**
```python
def test_get_stock_price_success(mocker):
    # 1. Siapkan Mock Response yang diinginkan
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "symbol": "AAPL",
        "price": 150.00
    }
    
    # 2. Patch HTTP Client agar mengembalikan mock_resp alih-alih menghubungi internet
    mocker.patch("httpx.Client.get", return_value=mock_resp)
    
    # 3. Panggil fungsi asli Anda
    result = get_stock_price("AAPL")
    
    # 4. Verifikasi (Assert) logika deterministik fungsi Anda (apakah membedah JSON dengan benar?)
    assert result["status"] == "success"
    assert "150.00" in result["report"]
```

### 2. Menguji Routing / Guardrail Agent (Integration Test)
Jika Anda mengubah logika instruksi pada instruksi awal Agent (misalnya menambah sub-agent baru), Anda harus memastikan bahwa Guardrail Callback dan framework Event ADK berjalan semestinya di `tests/integration/test_agents.py`.

Karena Pengujian Integrasi untuk Agent ADK bisa berurusan dengan _asynchronous call_, selalu gunakan *decorator* `@pytest.mark.asyncio`.

**Contoh Template Pengujian Guardrail / Routing:**
```python
import pytest
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from src.agents.smart_info_assistant.agent import smart_info_agent

@pytest.mark.asyncio
async def test_agent_behavior_or_guardrail():
    # 1. Setup session & runner dummy
    session_service = InMemorySessionService()
    await session_service.create_session("app", "user", "session_id")
    runner = Runner(agent=smart_info_agent, app_name="app", session_service=session_service)
    
    # 2. Siapkan payload pesan simulasi
    content = types.Content(role='user', parts=[types.Part(text="Kata Kunci Terlarang")])
    
    # 3. Jalankan Event Loop
    final_response = ""
    async for event in runner.run_async(user_id="user", session_id="session_id", new_message=content):
        # Tangkap respon finalnya
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break
            
    # 4. Verifikasi teks tanpa bergantung persis apakah LLM membalas kata per kata
    # (Contoh: kita pastikan callback kita menyela respon)
    assert "Pesan Error Ekspektasi" in final_response
```

---
*Happy Testing! "Keep it Fast, Keep it Green."* 🟢
