import unittest
import os
from unittest.mock import patch
from stt_engine import STTEngine

class TestSTTEngine(unittest.TestCase):
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"})
    def test_transcribe_whisper_file_not_found(self):
        engine = STTEngine()
        # Pass a non-existent file path
        result = engine.transcribe_whisper("non_existent_file.wav")
        # Assert that the result starts with the expected error message prefix
        self.assertTrue(result.startswith("Error in Whisper transcription:"))
        self.assertIn("No such file or directory", result)

if __name__ == '__main__':
    unittest.main()
