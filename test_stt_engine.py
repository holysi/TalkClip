import pytest
from unittest.mock import patch
from stt_engine import STTEngine

def test_refine_text_edge_cases():
    with patch('stt_engine.OpenAI') as mock_openai:
        # Instantiate engine, OpenAI key dependency is mocked
        engine = STTEngine()

        # Test empty input cases
        assert engine.refine_text(None) is None
        assert engine.refine_text("") == ""

        # Test error prefix cases
        assert engine.refine_text("Error: Some error message") == "Error: Some error message"
        assert engine.refine_text("Error") == "Error"
