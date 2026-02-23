import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class STTEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def transcribe_whisper(self, audio_path):
        """Transcribe audio using OpenAI Whisper API."""
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            return f"Error in Whisper transcription: {str(e)}"

    def transcribe_local(self, audio_path, model_key="qwen"):
        """
        Transcribe audio using local ASR API (supporting Qwen3, Breeze, etc.)
        model_key: "qwen" or "breeze"
        """
        api_url = os.getenv("LOCAL_ASR_API_URL", "http://localhost:8000/v1/audio/transcriptions")
        try:
            with open(audio_path, "rb") as f:
                response = requests.post(
                    api_url,
                    files={"file": f},
                    params={"model": model_key}
                )
            
            if response.status_code != 200:
                return f"Server Error ({response.status_code}): {response.text}"
                
            try:
                data = response.json()
            except Exception:
                return f"Error: Invalid JSON response from server: {response.text[:100]}"
                
            if "error" in data:
                return f"API Error: {data['error']}"
            return data.get("text", "Error: No text in response")
        except Exception as e:
            return f"Error in local ASR ({model_key}): {str(e)} (Ensure API is running)"

    def refine_text(self, text):
        """Refine text using GPT-4o-mini to remove filler words and polish."""
        if not text or text.startswith("Error"):
            return text
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一個專業的逐字稿整理助手。請幫我去除語音轉文字中的贅字（如：呃、然後、那個、um、uh 等），並在不改變原意的情況下，將句子潤飾得更流暢、口語化且正確。直接輸出結果即可，不要有其他廢話。"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in refinement: {str(e)}"
