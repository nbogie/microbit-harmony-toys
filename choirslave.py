from microbit import *
import music
import radio
import random
import microbit

chords = {
    'I': ["C3:1", "E4:1", "G4:1", "B4:1"], 
    'ii': ["D3:1", "F4:1", "A4:1", "C5:1"], 
    'II': ["D3:1", "F#4:1", "A4:1", "C5:1"], 
    'iii': ["E3:1", "G4:1", "B4:1", "D5:1"], 
    'III': ["E3:1", "G#4:1", "B4:1", "D5:1"], 
    'IV': ["F3:1", "A4:1", "C5:1", "E5:1"], 
    'iv': ["F3:1", "Ab4:1", "C5:1", "E5:1"], 
    'V': ["G3:1", "B4:1", "D5:1", "F5:1"], 
    'v': ["G3:1", "Bb4:1", "D5:1", "F5:1"], 
    'vi': ["A3:1", "C5:1", "E5:1", "G5:1"], 
    'VI': ["A3:1", "C#5:1", "E5:1", "G5:1"], 
    'vii': ["B3:1", "D5:1", "F5:1", "A5:1"]
    }



beatIx = 0
partIx = 0
chordName = '' #received from master

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        beatIx = 0
    noteName = chords[chordName][partIx]
    if (beatIx != 0 and random.random() > 0.9):
        noteName = "R:1"
    music.play(noteName)
    beatIx = beatIx + 1

def incPartIx(offset):
    global partIx
    partIx = partIx + offset
    if (partIx > 3):
        partIx = 0
    if (partIx < 0):
        partIx = 3

radio.on()
display.show(Image.GHOST)
while True:

    msg = radio.receive()
    if (msg != None):
        #delays things, at least when double digits
        #display.show(msg)
        chordName = msg
    
    if (chordName != None and chordName != ''):
        playNextNote()

    if button_a.is_pressed():
        incPartIx(-1)

    if button_b.is_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        microbit.panic(0) #shut it up!  Require a restart.
