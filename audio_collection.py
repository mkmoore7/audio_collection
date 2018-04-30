import pyaudio
import wave
from appJar import gui
from itertools import count
import random
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
DATA_LOCATION = "/Users/meredithmoore/Dropbox/Research/audio_data_collection/data"
WAVE_OUTPUT_FILENAME = "file.wav"       #make this dynamic

counter = count(0)

app = gui("Audio Data Collection", "800x600")
prompt_id = []
audio = pyaudio.PyAudio()
num_prompts = 5


#import the prompts from timit_prompts.txt
prompts = np.load('timit_prompts.npy')

# prompts = [["prompt text goes here", "promptID"], ...]

digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

grandfather = "You wished to know all about my grandfather. Well, he is nearly 93 years old; " \
              "he dresses himself in an ancient black frock coat, usually minus several buttons; " \
              "yet he still thinks as swiftly as ever. A long, flowing beard clings to his chin, " \
              "giving those who observe him a pronounced feeling of the utmost respect. When he speaks, " \
              "his voice is just a bit cracked and quivers a trifle. Twice each day he plays skillfully " \
              "and with zest upon our small organ. Except in the winter when the ooze or snow or ice prevents," \
              " he slowly takes a short walk in the open air each day. We have often urged him to walk more " \
              "and smoke less, but he always answers, \"Banana oil!\" Grandfather likes to be modern in his language."

caterpillar = "Do you like amusement parks? Well, I sure do. To amuse myself, I went twice last spring. " \
              "My most MEMORABLE moment was riding on the Caterpillar, which is a gigantic roller coaster" \
              " high above the ground. When I saw how high the Caterpillar rose into the bright blue sky I " \
              "knew it was for me. After waiting in line for thirty minutes, I made it to the front where the " \
              "man measured my height to see if I was tall enough. I gave the man my coins, asked for change, " \
              "and jumped on the cart. Tick, tick, tick, the Caterpillar climbed slowly up the tracks." \
              " It went SO high I could see the parking lot. Boy was I SCARED! I thought to myself, " \
              "\"There's no turning back now.\" People were so scared they screamed as we swiftly zoomed fast, " \
              "fast, and faster along the tracks. As quickly as it started, the Caterpillar came to a stop. " \
              "Unfortunately, it was time to pack the car and drive home. That night I dreamt of the wild ride " \
              "on the Caterpillar. Taking a trip to the amusement park and riding on the Caterpillar was " \
              "my MOST memorable moment ever!"

#images


prompts = prompts[0:num_prompts][:]

def press(button):
    iter = next(counter)
    if iter < len(prompts):
        app.setLabelFont("title", 50)
        app.setLabel("title", prompts[iter][0])
    else:
        app.setLabel("title", grandfather)


def record(button):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print "recording..."
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):      #change this to a stop button
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"

iter = next(counter)
if  iter < len(prompts):
    app.setLabelFont(50)
    app.addLabel("title", prompts[iter][0])



app.addButton("Next", press)
app.addButton("Record", record)
app.setFont(18)
app.setBg("white")
print iter

app.go()
