from microbit import *
import music
import radio
import random
chords = [
    ["C4:1", "E4:1", "G4:1", "B4:1"], 
    ["D4:1", "F4:1", "A4:1", "C5:1"], 
    ["E4:1", "G4:1", "B4:1", "D5:1"], 
    ["F4:1", "A4:1", "C5:1", "E5:1"], 
    ["G4:1", "B4:1", "D5:1", "F5:1"], 
    ["A4:1", "C5:1", "E5:1", "G5:1"], 
    ["B4:1", "D5:1", "F5:1", "A5:1"],

    ["D4:1", "F#4:1", "A4:1", "C5:1"], 
    ["E4:1", "G#4:1", "B4:1", "D5:1"], 
    ["F4:1", "Ab4:1", "C5:1", "E5:1"], 
    ["A4:1", "C#5:1", "E5:1", "G5:1"] 
    ]


progIx = 0
beatIx = 0
progression = [1,9,4,11,2,11,5]
partIx = 0


def incProgIx():
    global progIx
    progIx = progIx + 1
    if (progIx >= len(progression)):
        progIx = 0;    
    chordIx = progression[progIx] - 1
    #delays things
    #display.show(str(chordIx))
    radio.send(str(chordIx))

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        incProgIx()
        beatIx = 0

    chordIx = progression[progIx] - 1
    noteName = chords[chordIx][partIx]
    if (beatIx != 0 and random.random() > 0.8):
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

def incIx(offset):
    global ix
    ix = ix + offset
    if (ix > 6):
        ix = 0;
    if (ix < 0):
        ix = 6;
    display.show(str(ix + 1));


display.show(Image.PACMAN)
radio.on()

while True:
    playNextNote()

    if button_a.is_pressed():
        incPartIx(-1)

    if button_b.is_pressed():
        incPartIx(1)
