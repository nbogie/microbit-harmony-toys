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

beatIx = 0
partIx = 0
chordIx = 0 #received from master

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        beatIx = 0
    noteName = chords[chordIx][partIx]
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
    playNextNote()

    msg = radio.receive()
    if (msg != None):
        #delays things, at least when double digits
        #display.show(msg)
        chordIx = int(msg)

    if button_a.is_pressed():
        incPartIx(-1)

    if button_b.is_pressed():
        incPartIx(1)
