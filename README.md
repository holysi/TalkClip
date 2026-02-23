# TalkClip 使用說明書

這是一個基於 Python 的全域語音轉文字工具，專為 Windows 設計。

## 功能特點
- **全域熱鍵**：在任何視窗按住 `Right Alt` 即可錄音。
- **智能潤飾**：自動移除「呃、然後」等贅字。
- **自動複製**：轉換完成後自動存入剪貼簿。
- **雙模型支援**：支援 OpenAI Whisper (雲端) 與 Qwen3-ASR (可接本地)。

## 安裝步驟

1. **安裝 Python**: 確保你的系統已安裝 Python 3.10 或更高版本。
2. **安裝依賴庫**:
   開啟終端機 (PowerShell/CMD)，執行：
   ```bash
   pip install openai pynput pyaudio pyperclip requests python-dotenv
   ```
   > 注意：如果 `pyaudio` 安裝失敗，請先安裝 [PortAudio](http://portaudio.com/download.html) 或使用對應的 wheel 檔案。

3. **設定 API Key**:
   - 將 `.env.example` 重新命名為 `.env`。
   - 填入你的 `OPENAI_API_KEY`。

## 使用方法

1. 執行程式：
   ```bash
   python main.py
   ```
2. **錄音**：在任何地方按住鍵盤右側的 **Alt (Right Alt / AltGr)** 鍵。
3. **結束**：放開按鍵，等待 1-3 秒。
4. **貼上**：直接在目標位置 `Ctrl + V` 即可！

## Whisper-Local (CPU) 與 Breeze-ASR 模式

目前 TalkClip 已整合本地 ASR 伺服器，你只需要啟動 `main.py`，後端 API 就會自動在背景執行（不需要像舊版本那樣開兩個視窗）。

1. **安裝依賴庫**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install transformers fastapi uvicorn accelerate
   ```
2. **安裝 ffmpeg**:
   使用 `winget install ffmpeg` 即可。
3. **啟動主程式**:
   ```bash
   python main.py
   ```
4. **切換模式**:
   在 TalkClip 視窗中直接選擇 **Breeze-ASR** 或 **Whisper-Local (CPU)**。初次切換會自動下載模型，請稍候。

---

## 封裝為執行檔 (.exe)

如果你想將程式打包成一個單獨的 `.exe`，可以使用 `PyInstaller`：

1. **安裝 PyInstaller**:
   ```bash
   pip install pyinstaller
   ```
2. **進行打包**:
   ```bash
   pyinstaller --onefile --noconsole --name TalkClip main.py
   ```
   > [!NOTE]
   > 由於模型檔案很大 (數 GB)，模型權重通常會存放在使用者的快取目錄中，建議先執行 `python download_models.py` 確保模型已就緒。

---

## 鳴謝與開源授權 (Credits & Licenses)

TalkClip 整合了多個優秀的開源模型與技術：

- **OpenAI Whisper**: 由 OpenAI 開源的 ASR 模型。授權：[MIT License](https://github.com/openai/whisper/blob/main/LICENSE)。
- **MediaTek Breeze-ASR-25**: 由 MediaTek Research 研究開發的語音辨識模型。授權：Apache 2.0 基礎之授權。
- **OpenAI GPT-4o-mini**: 用於文本潤飾 (Refinement) 功能。
- **FastAPI / Uvicorn**: 提供高效能的本地 API 服務。
- **Transformers**: Hugging Face 推出的機器學習框架。
- **PyAudio / Pynput**: 提供音訊錄製與錄音熱鍵捕捉功能。

感謝開發者社群對開源專案的貢獻！
