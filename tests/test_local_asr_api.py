import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

from local_asr_api import app

client = TestClient(app)

def test_transcribe_happy_path():
    with patch("local_asr_api.get_pipeline") as mock_get_pipeline:
        mock_pipe = MagicMock()
        mock_pipe.return_value = {"text": "Hello world"}
        mock_get_pipeline.return_value = mock_pipe

        # Create dummy file content
        file_content = b"dummy audio content"
        files = {"file": ("test.wav", file_content, "audio/wav")}

        response = client.post("/v1/audio/transcriptions?model=whisper-local", files=files)

        assert response.status_code == 200
        assert response.json() == {"text": "Hello world"}

        # Check that get_pipeline was called with the mapped model
        mock_get_pipeline.assert_called_once_with("openai/whisper-base")

        # Check that the mock pipe was called (the argument is a temp file path)
        mock_pipe.assert_called_once()
        args, _ = mock_pipe.call_args
        temp_file_passed = args[0]
        assert temp_file_passed == "temp_api_audio.wav"

        # Ensure temp file is cleaned up after success
        assert not os.path.exists("temp_api_audio.wav")

def test_transcribe_breeze_model_mapping():
    with patch("local_asr_api.get_pipeline") as mock_get_pipeline:
        mock_pipe = MagicMock()
        mock_pipe.return_value = {"text": "Breeze result"}
        mock_get_pipeline.return_value = mock_pipe

        files = {"file": ("test.wav", b"dummy", "audio/wav")}

        response = client.post("/v1/audio/transcriptions?model=breeze", files=files)

        assert response.status_code == 200
        assert response.json() == {"text": "Breeze result"}

        # Check that get_pipeline was called with the Breeze HF ID
        mock_get_pipeline.assert_called_once_with("MediaTek-Research/Breeze-ASR-25")

def test_transcribe_unmapped_model():
    with patch("local_asr_api.get_pipeline") as mock_get_pipeline:
        mock_pipe = MagicMock()
        mock_pipe.return_value = {"text": "Custom result"}
        mock_get_pipeline.return_value = mock_pipe

        files = {"file": ("test.wav", b"dummy", "audio/wav")}

        response = client.post("/v1/audio/transcriptions?model=custom/model-id", files=files)

        assert response.status_code == 200
        assert response.json() == {"text": "Custom result"}

        # Unmapped models should be passed through as-is
        mock_get_pipeline.assert_called_once_with("custom/model-id")

def test_transcribe_model_load_error():
    with patch("local_asr_api.get_pipeline") as mock_get_pipeline:
        mock_get_pipeline.side_effect = Exception("Model not found")

        files = {"file": ("test.wav", b"dummy", "audio/wav")}
        response = client.post("/v1/audio/transcriptions?model=unknown-model", files=files)

        assert response.status_code == 200
        json_resp = response.json()
        assert "error" in json_resp
        assert "unknown-model" in json_resp["error"]
        assert "Model not found" in json_resp["error"]

def test_transcribe_inference_error():
    with patch("local_asr_api.get_pipeline") as mock_get_pipeline:
        mock_pipe = MagicMock()
        mock_pipe.side_effect = Exception("Inference failed")
        mock_get_pipeline.return_value = mock_pipe

        files = {"file": ("test.wav", b"dummy", "audio/wav")}
        response = client.post("/v1/audio/transcriptions?model=whisper-local", files=files)

        assert response.status_code == 200
        json_resp = response.json()
        assert "error" in json_resp
        assert "Inference failed" in json_resp["error"]

        # Ensure temp file is cleaned up after an exception
        assert not os.path.exists("temp_api_audio.wav")
