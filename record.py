import pyaudio
import wave

import pygame, sys
from pygame.locals import *

pygame.init()
scr = pygame.display.set_mode((640, 480))
recording = True

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

while True:
    if recording:
        data = stream.read(CHUNK)
        frames.append(data)

    for event in pygame.event.get():
        if event.type == KEYDOWN and recording:
            print("* done recording")
            print recording

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            recording = False


        if event.type == QUIT:
            pygame.quit(); sys.exit()