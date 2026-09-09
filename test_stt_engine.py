import unittest
from unittest.mock import patch, MagicMock, mock_open
import os

from stt_engine import STTEngine

class TestSTTEngine(unittest.TestCase):
    @patch('stt_engine.os.getenv')
    @patch('stt_engine.OpenAI')
    def setUp(self, MockOpenAI, mock_getenv):
        mock_getenv.return_value = "fake_api_key"
        self.mock_openai_client = MagicMock()
        MockOpenAI.return_value = self.mock_openai_client
        self.engine = STTEngine()

    @patch('builtins.open', new_callable=mock_open, read_data=b"fake audio data")
    def test_transcribe_whisper_success(self, mock_file):
        """Test happy path for transcribe_whisper."""
        # Setup mock for OpenAI transcriptions create
        mock_response = MagicMock()
        mock_response.text = "This is a test transcript."
        self.mock_openai_client.audio.transcriptions.create.return_value = mock_response

        # Execute
        result = self.engine.transcribe_whisper("fake_path.wav")

        # Verify
        self.assertEqual(result, "This is a test transcript.")
        mock_file.assert_called_once_with("fake_path.wav", "rb")
        self.mock_openai_client.audio.transcriptions.create.assert_called_once()
        args, kwargs = self.mock_openai_client.audio.transcriptions.create.call_args
        self.assertEqual(kwargs['model'], "whisper-1")
        self.assertEqual(kwargs['file'], mock_file())

    @patch('builtins.open', new_callable=mock_open, read_data=b"fake audio data")
    def test_transcribe_whisper_api_error(self, mock_file):
        """Test API error path for transcribe_whisper."""
        # Setup mock for OpenAI transcriptions create to raise Exception
        self.mock_openai_client.audio.transcriptions.create.side_effect = Exception("API rate limit exceeded")

        # Execute
        result = self.engine.transcribe_whisper("fake_path.wav")

        # Verify
        self.assertEqual(result, "Error in Whisper transcription: API rate limit exceeded")
        mock_file.assert_called_once_with("fake_path.wav", "rb")
        self.mock_openai_client.audio.transcriptions.create.assert_called_once()

    def test_transcribe_whisper_file_io_error(self):
        """Test File IO error path for transcribe_whisper."""
        # Note: We don't mock 'open' here so it raises FileNotFoundError for real,
        # but to ensure safety and isolation we can mock it to raise an exception.
        with patch('builtins.open', side_effect=FileNotFoundError("No such file or directory")):
            # Execute
            result = self.engine.transcribe_whisper("nonexistent.wav")

            # Verify
            self.assertEqual(result, "Error in Whisper transcription: No such file or directory")
            self.mock_openai_client.audio.transcriptions.create.assert_not_called()

if __name__ == '__main__':
    unittest.main()
