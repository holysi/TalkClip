import unittest
from unittest.mock import patch, MagicMock
from recorder import Recorder

class TestRecorder(unittest.TestCase):
    @patch('recorder.pyaudio.PyAudio')
    def setUp(self, mock_pyaudio):
        # We patch pyaudio.PyAudio globally in setUp to prevent actual hardware access
        self.mock_pyaudio_instance = mock_pyaudio.return_value
        self.recorder = Recorder("test_recording.wav")
        # Ensure that Recorder uses our mocked instance
        self.recorder.p = self.mock_pyaudio_instance
        self.recorder.stream = MagicMock()

    def test_stop_when_not_recording(self):
        # Set explicitly to False
        self.recorder.is_recording = False

        result = self.recorder.stop()

        self.assertIsNone(result)
        self.recorder.stream.stop_stream.assert_not_called()
        self.recorder.stream.close.assert_not_called()

    @patch('recorder.wave.open')
    @patch('builtins.print')
    def test_stop_when_recording(self, mock_print, mock_wave_open):
        self.recorder.is_recording = True
        self.recorder.frames = [b'frame1', b'frame2']
        self.mock_pyaudio_instance.get_sample_size.return_value = 2

        mock_wf = MagicMock()
        mock_wave_open.return_value = mock_wf

        result = self.recorder.stop()

        # Assert state changes
        self.assertFalse(self.recorder.is_recording)

        # Assert stream was closed
        self.recorder.stream.stop_stream.assert_called_once()
        self.recorder.stream.close.assert_called_once()

        # Assert wave functions were called with correct parameters
        mock_wave_open.assert_called_once_with("test_recording.wav", 'wb')
        mock_wf.setnchannels.assert_called_once_with(1)
        mock_wf.setsampwidth.assert_called_once_with(2)
        mock_wf.setframerate.assert_called_once_with(44100)
        mock_wf.writeframes.assert_called_once_with(b'frame1frame2')
        mock_wf.close.assert_called_once()

        # Assert return value is the filename
        self.assertEqual(result, "test_recording.wav")

if __name__ == '__main__':
    unittest.main()
