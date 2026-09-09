import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

models = [
    "MediaTek-Research/Breeze-ASR-25",
    "openai/whisper-base"
]

def download_models():
    for model_id in models:
        print(f"\n--- Downloading model: {model_id} ---")
        try:
            # Check if GPU is available to determine dtype
            has_gpu = torch.cuda.is_available()
            torch_dtype = torch.float16 if has_gpu else torch.float32
            
            print(f"Loading processor for {model_id}...")
            AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
            
            print(f"Loading model {model_id}...")
            AutoModelForSpeechSeq2Seq.from_pretrained(
                model_id, 
                torch_dtype=torch_dtype, 
                low_cpu_mem_usage=True, 
                use_safetensors=True,
                trust_remote_code=True
            )
            print(f"Successfully downloaded {model_id}")
        except Exception as e:
            print(f"Error downloading {model_id}: {e}")

if __name__ == "__main__":
    download_models()
    print("\nAll model downloads requested complete.")
