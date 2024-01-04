import wave
from io import BytesIO

class AudioInputBuffer : 
    
    def __create_buffer(self):
        self.buffer = BytesIO()
        self.buffer.name = "output.wav"

    def __init__(self, channels, samplesize, rate):
        self.__create_buffer()
        self.wf = wave.open(self.buffer, 'wb')
        self.wf.setnchannels(channels)
        self.wf.setsampwidth(samplesize)
        self.wf.setframerate(rate)


    def writeframes(self, frames):
        self.wf.writeframes(frames)
        
    def close(self):
        self.wf.close()

