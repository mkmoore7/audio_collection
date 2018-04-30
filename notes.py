#N listeners
#M speakers, files encoded as speakercode_batchnumber_promptnumber.wav (FO2_B1_UA99.wav)

#x words spoken


#Each listener has a list of files that they need to listen to and evaluate
L1 = ["F02_B1_UA99.wav", ...]


#Each speaker needs to have a total Word Error Rate and accuracy by the end of it
speakers_wer = [ [F01_numerator, F01_denominator], [F02_numerator, F02_denominator], ... , [M_numerator, M_denominator]]
speakers_boolean = [ [F01_numerator, F01_denominator], [F02_numerator, F02_denominator], ... , [M_numerator, M_denominator]]


#We set the listener to their username, and load the list of filenames associated with that specific listener

#they go through the list of filenames, and watch/listen to the media,
#after each video/audio segment, they transcribe what they thought was said
#This is entered into a text box, which is then validated
## to see if it was the same as what it was supposed to be (the groundtruth/prompt)

#with this, we update the speaker array, add the WER (which we can do as boolean or as a WER, or both actually),
#and update the denominator as well



def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    # build the matrix
    d = editDistance(r, h)

    result = float(d[len(r)][len(h)]) / len(r)
    return result