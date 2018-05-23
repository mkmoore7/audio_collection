import Tkinter as tk
import threading
import numpy as np
from itertools import count


SPEAKER_ID = '000'
prompts = None
num_timit_prompts = 20

class App():
    def __init__(self, master):
        #set up the prompts
        timit_prompts = np.load('timit_prompts.npy')
        self.prompts = []
        self.prompts.append(['Please count from 1 to 10', 'digits'])
        for x in range(num_timit_prompts):
            self.prompts.append(timit_prompts[x][:])

        self.prompts.append(['Please read the grandfather passage', 'gpa'])
        self.prompts.append(['Please read the caterpillar passage', 'caterpillar'])
        self.prompts.append(['Please read the rainbow passage', 'rainbow'])
        self.prompts.append(['Please describe the photo below: ', 'img1'])
        self.prompts.append(['Please describe the photo below: ', 'img2'])
        self.prompts.append(['Please describe the photo below: ', 'img3'])
        self.prompts.append(['Please describe the photo below: ', 'img4'])
        self.prompts.append(['Please describe the photo below: ', 'img5'])

        self.counter = count(0)

        self.isrecording = False
        self.label = tk.Label(main, text="Prompts will appear here")
        self.next_button = tk.button(main, text= 'Next')
        self.rec_button = tk.Button(main, text='Record')
        self.stop_button = tk.Button(main, text = 'Stop')
        self.rec_button.bind("<Button-1>", self.startrecording)
        self.stop_button.bind("<Button-1>", self.stoprecording)
        self.label.pack()
        self.rec_button.pack()
        self.stop_button.pack()

    def get_filename(self, iter, ):
        filename = SPEAKER_ID + '_' + prompts[0][1]


    def startrecording(self, event):
        self.isrecording = True
        t = threading.Thread(target=self._record)
        t.start()

    def stoprecording(self, event):
        self.isrecording = False

    def next_prompt(self, event):



    def _record(self):
        while self.isrecording:
            print "Recording"
        print "Stopped recording"

main = tk.Tk()
app = App(main)
main.mainloop()