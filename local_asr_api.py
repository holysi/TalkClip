from fastapi import FastAPI, UploadFile, File, Query
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import traceback
import uvicorn
import shutil
import os

app = FastAPI()

# Loaded models dictionary to avoid reloading
loaded_pipes = {}

def get_pipeline(model_id: str):
    if model_id in loaded_pipes:
        return loaded_pipes[model_id]
    
    # Force CPU if NVIDIA GPU is not found or requested
    has_gpu = torch.cuda.is_available()
    device = "cuda:0" if has_gpu else "cpu"
    torch_dtype = torch.float16 if has_gpu else torch.float32

    print(f"Loading {model_id} to {device} (dtype: {torch_dtype})...")
    
    # Standard transformers pipeline logic
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, 
        torch_dtype=torch_dtype, 
        low_cpu_mem_usage=True, 
        use_safetensors=True,
        trust_remote_code=True
    )
    model.to(device)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )
    
    loaded_pipes[model_id] = pipe
    return pipe

@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...), 
    model: str = Query("whisper-local")
):
    # Mapping friendly names to HF IDs
    model_map = {
        "breeze": "MediaTek-Research/Breeze-ASR-25",
        "whisper-local": "openai/whisper-base" # Using 'base' for CPU; 'tiny' is faster but less accurate
    }
    # Validate the requested model against the whitelist
    if model.lower() in model_map:
        target_model = model_map[model.lower()]
    elif model in model_map.values():
        target_model = model
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Model '{model}' is not allowed. Supported models are: {', '.join(model_map.keys())}")

    print(f"Request received: model={model}, mapped={target_model}")
    
    try:
        pipe = get_pipeline(target_model)
    except Exception as e:
        error_msg = f"Failed to load model {target_model}: {str(e)}"
        print(f"ERROR: {error_msg}")
        return {"error": error_msg}

    temp_file = "temp_api_audio.wav"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run inference
    print("Running inference...")
    try:
        result = pipe(temp_file)
        os.remove(temp_file)
        print(f"Inference complete. Result length: {len(result.get('text', ''))}")
        return {"text": result["text"]}
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        error_msg = f"Inference error: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {"error": error_msg}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
