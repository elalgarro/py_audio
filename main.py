from pynput.keyboard import Key, Listener
import pyaudio, wave, sched, time, sys
from datetime import datetime
from openai import OpenAI
from io import BytesIO
client = OpenAI()
p = pyaudio.PyAudio()
frames = []
CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE= 44100


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(Listener) : 

    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        if key.char == 'r':
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key.char == 'r':
            self.key_pressed = False
        return True

listener = MyListener()
listener.start()
started = False
stream = None
class WavFileBuilder : 

    def __init__(self):
        _time = datetime.now()
        filename = f"output/{datetime.timestamp(_time)}.wav" 
        self.buffer = BytesIO()
        self.buffer.name = "output.wav"
        self.wf = wave.open(self.buffer, 'wb')
        self.filename = filename
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)


    def writeframes(self, frames):
        self.wf.writeframes(frames)
        
    def close(self):
        self.wf.close()


def get_transcript(filebuilder):
    transcript = client.audio.transcriptions.create(
           model="whisper-1",
           file=filebuilder.buffer
            )
    print(transcript)

def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        try:
            stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = callback)
            print("Stream active:", stream.is_active())
            started = True
            print("start Stream")
        except:
            raise

    elif not listener.key_pressed and started:
        print("Stop recording")
        stream.stop_stream()
        stream.close()
        #p.terminate()
        wf = WavFileBuilder()
        wf.writeframes(b''.join(frames))
        wf.close()
        get_transcript(wf)
        frames = []
        started = False
        # sys.exit()
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())


print("Press and hold the 'r' key to begin recording") 
print("Release the 'r' key to end recording") 
task = sched.scheduler(time.time, time.sleep)
task.enter(0.1, 1, recorder, ())
task.run()
