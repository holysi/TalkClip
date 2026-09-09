import wave
import pyaudio
import threading
from datetime import datetime

class Recorder:
    def __init__(self, filename="temp_recording.wav"):
        self.filename = filename
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None

    def start(self):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.frames = []
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        
        threading.Thread(target=self._record).start()
        print("Recording started...")

    def _record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop(self):
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Recording saved to {self.filename}")
        return self.filename
