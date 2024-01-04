import pyaudio, wave, sched, time, sys
from datetime import datetime
from openai import OpenAI
from io import BytesIO
from src.listener import MyListener
from src.audio_input_buffer import AudioInputBuffer
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

listener = MyListener()
listener.start()
started = False
stream = None

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
        wf = AudioInputBuffer(CHANNELS, p.get_sample_size(FORMAT), RATE)
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
