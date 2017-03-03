from microbit import *
import music
import radio
import random
import speech

#Instructions: Press A to sing a note and tell listeners about it.
#                 Listeners will sing a note above it, and tell, too.
#                 Between two micro:bits, it will bounce back and forth,
#                 but between 3 or more microbits, crazy things will happen.
#              Press B to change voice to a new random one.

pitches = [115, 103, 94, 88, 78, 70, 62, 58, 52, 46, 44, 39, 35, 31, 29, 26, 23, 22]

class Voice:
    def __init__(self):
        self.throat = 128
        self.mouth = 128
        
    def change(self):
        self.throat = random.randint(0,255)
        self.mouth = random.randint(0,255)

def curwenSign(sd):
    images = [
        Image(
        "00000:"
        "79999:"
        "99639:"
        "59659:"
        "02980"
        )
        , Image(
        "00009:"
        "00090:"
        "00900:"
        "09000:"
        "90000"
        )
        , Image(
        "00000:"
        "00000:"
        "99999:"
        "00000:"
        "00000"
        )
        , Image(
        "99997:"
        "99997:"
        "99997:"
        "97000:"
        "97000"
        )
        , Image(
        "00000:"
        "99800:"
        "99984:"
        "99999:"
        "99972"
        )
        , Image(
        "00000:"
        "99990:"
        "09094:"
        "05009:"
        "00007"
        )
        , Image(
        "00099:"
        "00900:"
        "69600:"
        "95960:"
        "99600"
        )]
    return images[sd]

#return a pitched phoneme string for the given scale degree (count from 0)
#e.g. solfaPhoneme(0) returns "#115DOWWWWWWW", 
#e.g. solfaPhoneme(4) returns "#78SOHWWWW"
#This string can then be passed to speech.sing(str)
#These pitches are from the C Major scale, currently.
def solfaPhoneme(n=None):
    global pitches
    if n == None:
        n = random.randint(0, len(pitches)-1)
        
    phonemes = [
        "DOWWWWWW",   # Doh
        "REYYYYYY",   # Re
        "MIYYYYYY",    # Mi
        "FAOAOAOAOR",  # Fa
        "SOHWWWWW",    # Soh
        "LAOAOAOAOR",  # La
        "TIYYYYYY"    # Ti
    ]
    if n >= len(pitches):
        n = n % 7
    pitch = pitches[n]
    phoneme = phonemes[n % 7]
    #e.g. return "#115DOWWWWWW"
    return "#{}{}".format(str(pitch), phoneme)

#speech.sing  the given phoneme, using my voice
def voiceSing(phoneme):
    speech.sing(phoneme, speed=80, throat=myVoice.throat, mouth=myVoice.mouth)
    
def singThenTell(sd):
    phoneme = solfaPhoneme(sd)
    display.show(curwenSign(sd % 7), delay=50, wait=False)
    voiceSing(phoneme)
    radio.send(str(sd))        

def mainLoop():
    currentScaleDegree = 0;
    while True:
        global myVoice
        
        if button_a.was_pressed():
            singThenTell(0)
            currentScaleDegree = 0
        
        msg = radio.receive()
        if (msg != None):
            currentScaleDegree = (int(msg) + 1) % 14
            singThenTell(currentScaleDegree)

        if button_b.was_pressed():
            myVoice.change()
            voiceSing(solfaPhoneme(currentScaleDegree))

myVoice = Voice()
radio.config(channel=20, group=20)
radio.on()
display.show(Image.MUSIC_QUAVERS, wait=False)
mainLoop()
