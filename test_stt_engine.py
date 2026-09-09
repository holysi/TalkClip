import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from stt_engine import STTEngine

class TestSTTEngine(unittest.TestCase):
    @patch('stt_engine.OpenAI')
    def setUp(self, mock_openai):
        # Prevent the OpenAI client from actually initializing and requiring an API key
        self.engine = STTEngine()
        self.mock_openai = mock_openai

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_success(self, mock_file, mock_post):
        """Test successful local transcription."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "Hello world"}
        mock_post.return_value = mock_response

        result = self.engine.transcribe_local("dummy.wav", model_key="qwen")

        self.assertEqual(result, "Hello world")
        mock_post.assert_called_once()
        mock_file.assert_called_once_with("dummy.wav", "rb")

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_server_error(self, mock_file, mock_post):
        """Test local transcription when server returns non-200 status."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        result = self.engine.transcribe_local("dummy.wav")

        self.assertIn("Server Error (500)", result)
        self.assertIn("Internal Server Error", result)

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_invalid_json(self, mock_file, mock_post):
        """Test local transcription when server returns invalid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("JSON Decode Error")
        mock_response.text = "Bad JSON Data"
        mock_post.return_value = mock_response

        result = self.engine.transcribe_local("dummy.wav")

        self.assertIn("Error: Invalid JSON response", result)
        self.assertIn("Bad JSON Data", result)

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_api_error(self, mock_file, mock_post):
        """Test local transcription when server returns a JSON with an error field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "Model not found"}
        mock_post.return_value = mock_response

        result = self.engine.transcribe_local("dummy.wav")

        self.assertIn("API Error: Model not found", result)

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_no_text(self, mock_file, mock_post):
        """Test local transcription when JSON response is missing the 'text' key."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"something_else": "value"}
        mock_post.return_value = mock_response

        result = self.engine.transcribe_local("dummy.wav")

        self.assertEqual(result, "Error: No text in response")

    @patch('stt_engine.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b"dummy audio data")
    def test_transcribe_local_exception(self, mock_file, mock_post):
        """Test local transcription when requests.post raises an exception (e.g. network error)."""
        mock_post.side_effect = Exception("Connection Refused")

        result = self.engine.transcribe_local("dummy.wav", model_key="breeze")

        self.assertIn("Error in local ASR (breeze)", result)
        self.assertIn("Connection Refused", result)

if __name__ == '__main__':
    unittest.main()
