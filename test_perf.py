import time
import asyncio
import httpx
import uvicorn
import multiprocessing
from local_asr_api import app

def run_server():
    # Patch the get_pipeline to return a fake pipeline that sleeps
    from local_asr_api import get_pipeline, loaded_pipes
    import local_asr_api
    class FakePipe:
        def __call__(self, file_path):
            import time
            time.sleep(1) # Simulate slow inference
            return {"text": "mocked text"}

    local_asr_api.get_pipeline = lambda model_id: FakePipe()
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

async def make_request(client, dummy_wav):
    files = {'file': ('dummy.wav', dummy_wav, 'audio/wav')}
    start = time.time()
    resp = await client.post("http://127.0.0.1:8001/v1/audio/transcriptions?model=whisper-local", files=files)
    end = time.time()
    return end - start

async def main():
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()

    # Wait for server to start
    time.sleep(2)

    dummy_wav = b"RIFF$" + b"\x00"*40 # dummy valid-ish file or just bytes

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Warmup
        try:
            await make_request(client, dummy_wav)
        except Exception:
            pass

        start_time = time.time()
        # Run 5 requests concurrently
        tasks = [make_request(client, dummy_wav) for _ in range(5)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        print(f"Individual request times: {results}")
        print(f"Total time for 5 concurrent requests: {total_time:.2f}s")

    server_process.terminate()
    server_process.join()

if __name__ == "__main__":
    asyncio.run(main())
