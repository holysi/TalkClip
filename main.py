import tkinter as tk
from tkinter import ttk
import threading
import pyperclip
from pynput import keyboard
from recorder import Recorder
from stt_engine import STTEngine
from dotenv import load_dotenv
import uvicorn
from local_asr_api import app as asr_app

load_dotenv()

class VoiceToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TalkClip")
        self.root.geometry("400x250")
        self.root.attributes("-topmost", True)  # Keep window on top
        
        self.recorder = Recorder()
        self.stt = STTEngine()
        
        self.is_alt_pressed = False
        self.processing = False
        
        self.setup_ui()
        self.setup_hotkeys()
        self.start_local_server()

    def start_local_server(self):
        """Start the local ASR API server in a separate thread."""
        def run_server():
            # Run uvicorn on a local thread
            uvicorn.run(asr_app, host="127.0.0.1", port=8000, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        print("Local ASR server started in background.")

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="準備就緒", font=("Microsoft JhengHei", 12))
        self.status_label.pack(pady=20)
        
        self.hint_label = tk.Label(self.root, text="按住 [Right Alt] 開始錄音\n放開後自動轉文字並複製", font=("Microsoft JhengHei", 10), fg="gray")
        self.hint_label.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="whisper")
        self.whisper_rb = ttk.Radiobutton(self.root, text="OpenAI Whisper (Cloud)", variable=self.mode_var, value="whisper")
        self.whisper_rb.pack()

        self.breeze_rb = ttk.Radiobutton(self.root, text="Breeze-ASR (Local)", variable=self.mode_var, value="breeze")
        self.breeze_rb.pack()

        self.whisper_local_rb = ttk.Radiobutton(self.root, text="Whisper-Local (CPU)", variable=self.mode_var, value="whisper-local")
        self.whisper_local_rb.pack()

        # Added Refinement Toggle
        self.refine_var = tk.BooleanVar(value=False)
        self.refine_cb = ttk.Checkbutton(self.root, text="AI 內文潤飾 (需 OpenAI Key)", variable=self.refine_var)
        self.refine_cb.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate')

    def update_status(self, text, color="black"):
        self.status_label.config(text=text, fg=color)

    def setup_hotkeys(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        # Detect Right Alt (alt_gr)
        if key == keyboard.Key.alt_gr and not self.is_alt_pressed and not self.processing:
            self.is_alt_pressed = True
            self.root.after(0, lambda: self.update_status("正在錄音...", "red"))
            self.recorder.start()

    def on_release(self, key):
        if key == keyboard.Key.alt_gr and self.is_alt_pressed:
            self.is_alt_pressed = False
            self.root.after(0, lambda: self.update_status("處理中...", "blue"))
            self.root.after(0, lambda: self.progress.pack(pady=5))
            self.root.after(0, lambda: self.progress.start())
            
            audio_file = self.recorder.stop()
            threading.Thread(target=self.process_audio, args=(audio_file,)).start()

    def process_audio(self, audio_file):
        self.processing = True
        try:
            mode = self.mode_var.get()
            if mode == "whisper":
                raw_text = self.stt.transcribe_whisper(audio_file)
            else:
                # Local models (qwen, breeze)
                raw_text = self.stt.transcribe_local(audio_file, model_key=mode)
            
            # Conditionally refine text
            if self.refine_var.get() and raw_text and not raw_text.startswith("Error"):
                refined_text = self.stt.refine_text(raw_text)
            else:
                refined_text = raw_text
            
            pyperclip.copy(refined_text)
            
            self.root.after(0, lambda: self.update_status("已複製到剪貼簿！", "green"))
            print(f"Result: {refined_text}")
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"錯誤: {str(e)}", "red"))
        finally:
            self.processing = False
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.progress.pack_forget())

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()
