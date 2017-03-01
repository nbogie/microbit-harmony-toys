from microbit import *
import music
import radio
import random
import microbit

chords = {
    'I': ["C3", "E4", "G4", "B4"], 
    '#Idim': ["C#3", "E4", "G4", "Bb4"], 
    'ii': ["D3", "F4", "A4", "C5"], 
    'II': ["D3", "F#4", "A4", "C5"], 
    'iii': ["E3", "G4", "B4", "D5"], 
    'III': ["E3", "G#4", "B4", "D5"], 
    'IV': ["F3", "A4", "C5", "E5"], 
    '#IVdim': ["F#3", "A4", "C5", "Eb5"], 
    'iv': ["F3", "Ab4", "C5", "E5"], 
    'V': ["G3", "B4", "D5", "G5"], #omit 7th
    '#Vdim': ["G#3", "B4", "D5", "F5"], 
    'v': ["G3", "Bb4", "D5", "F5"], 
    'vi': ["A3", "C5", "E5", "G5"], 
    'VI': ["A3", "C#5", "E5", "G5"], 
    'vii': ["B3", "D5", "F5", "A5"]
}

scale = "C D E F G A B".split(' ')

isCycling = True

beatIx = 0
partIx = 1
chordName = '' #received from master

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        beatIx = 0

    if beatIx == 15:
        noteName = "" #don't even play a rest.  hack to be ready to hear new chord.
    elif (beatIx != 0 and random.random() > 0.9):
        noteName = "R"
    else:
        noteName = chords[chordName][partIx]
        if isCycling:
            incPartIx(1) 
    
    if noteName != '':
        music.play(noteName + ":1")

    beatIx = beatIx + 1

def incPartIx(offset):
    global partIx
    partIx = partIx + offset
    if (partIx > 3):
        partIx = 0
    if (partIx < 0):
        partIx = 3


radio.on()

display.show(Image.GHOST, wait=False)

while True:

    msg = radio.receive()
    if (msg != None):
        chordName = msg
        beatIx = 0
        display.scroll(chordName, delay=70, wait=False, loop=False, monospace=False)

    if (chordName != None and chordName != ''):
        if beatIx < 16:
            playNextNote()

    if button_a.was_pressed():
        incPartIx(-1)

    if button_b.was_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        microbit.panic(0) #shut it up!  Require a restart.
