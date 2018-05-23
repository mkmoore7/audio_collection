import pyaudio
import wave
from appJar import gui
from itertools import count
import numpy as np


SPEAKER_ID = '000'

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
DATA_LOCATION = "/Volumes/Babelfish/test"
recording = False
counter = count(0)

app = gui("Audio Data Collection", "800x400")
prompt_id = []
audio = pyaudio.PyAudio()
num_timit_prompts = 15


class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode

        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        if self._stream == None:
            print 'stream == None'
        self._stream.start_stream()
        print 'recording started...'
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        print 'recording finished.'
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile



def record(button):
    filename = 'test'
    rec = Recorder(channels=2)
    with rec.open(filename + '.wav', 'wb') as recfile2:
        if button == 'Record':
            recfile2.start_recording()
        if button == 'Stop':
            recfile2.stop_recording()


def press(button):
    iter = next(counter)
    if iter < len(prompts):
        app.setLabelFont("title", 80)
        app.setLabel("title", prompts[iter][0])
        global filename
        filename = SPEAKER_ID + '_' + prompts[iter][1]
        print filename
    else:
        app.setLabel("title", "Thank you, you have completed the study")



# import the prompts from timit_prompts.txt
timit_prompts = np.load('timit_prompts.npy')

digits = 'Please count from 1 to 10.'
# digits, then timit prompts, then longer grandfather and rainbow and caterpillar
prompts = [[digits, 'digits']]
for x in range(num_timit_prompts):
    prompts.append(timit_prompts[x][:])

prompts.append(['Please read the grandfather passage', 'gpa'])
prompts.append(['Please read the caterpillar passage', 'caterpillar'])
prompts.append(['Please read the rainbow passage', 'rainbow'])
prompts.append(['Please describe the photo below: ', 'img1'])
prompts.append(['Please describe the photo below: ', 'img2'])
prompts.append(['Please describe the photo below: ', 'img3'])
prompts.append(['Please describe the photo below: ', 'img4'])
prompts.append(['Please describe the photo below: ', 'img5'])

print prompts

filename = SPEAKER_ID + '_' + prompts[0][1]
print filename

iter = next(counter)
if iter < len(prompts):
    app.setLabelFont(80)
    app.addLabel("title", prompts[iter][0])



#app.addImage("img1", "img1.jpg")

app.addButton("Next", press)
app.addButton("Record", record)
app.addButton("Stop", record)
app.setFont(18)
app.setBg("white")


app.go()
