import wave
from appJar import gui
from itertools import count
import numpy as np
import cv2
from os import path
import pyaudio
import pygame, sys
from pygame.locals import *


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



# import the prompts from timit_prompts.txt
timit_prompts = np.load('timit_prompts.npy')

digits = 'Please count from 1 to 10.'

#digits, then timit prompts, then longer grandfather and rainbow and caterpillar
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

def press(button):
    iter = next(counter)
    print iter

    if iter < len(prompts):
        app.setLabelFont("title", 80)
        app.setLabel("title", prompts[iter][0])
        global filename
        filename = SPEAKER_ID + '_' + prompts[iter][1]
        print filename
    else:
        app.setLabel("title", "Thank you, you have completed the study")


def record(button):
    pygame.init()
    scr = pygame.display.set_mode((640, 480))
    recording = True

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    WAVE_OUTPUT_FILENAME = filename + '.wav'

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

        if button == 'Stop' and recording:
            print("* done recording")
            stream.stop_stream()
            stream.close()
            p.terminate()

            print 'saving .wav'
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            recording = False


    #VIDEO RECORDING HERE
    '''
    print('[INFO] Warming up camera...')
    cap = cv2.VideoCapture(0)
    time.sleep(0.1)
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter((outfile+'.mp4'), fourcc, 20.0, (640, 360))

    fps = 15
    capSize = (1280, 720)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(outfile+'.mp4', fourcc, fps, capSize)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #write the flipped frame
            out.write(frame)
            cv2.imshow('frame', frame)
            #TODO: Figure out how to stop using a different button
            if cv2.waitKey(1) &0xFF == ord('q') or not recording:
                break
        else:
            print 'frame not read correctly'
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    '''


    #once record is pressed again, move on to the next prompt




iter = next(counter)
if iter < len(prompts):
    app.setLabelFont(80)
    app.addLabel("title", prompts[iter][0])




#app.addImage("img1", "img1.jpg")

app.addButton("Next", press)
#app.addButton("Record", record)
#app.addButton("Stop", record)
app.setFont(24)
app.setBg("white")


app.go()
