from microbit import *
import music
import radio
import random
import microbit

#TODO: remember and repeat the randomly generated ostinato
#TODO: R + 10th is nice
#TODO: 3 + 5 is nice (rootless)
#TODO: persist a programmed chord progression

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


progIx = 0
beatIx = 0
#progression = "I|III|IV|VI|ii|VI|V".split('|')
progression = "vi|V|I|IV".split('|')
partIx = 0


def incProgIx():
    global progIx
    progIx = progIx + 1
    if (progIx >= len(progression)):
        progIx = 0;    
    chordName = progression[progIx]
    #delays things
    #display.show(chordName)
    display.scroll(chordName, delay=100, wait=False, loop=False, monospace=False)

    radio.send(chordName)

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        incProgIx()
        beatIx = 0

    chordName = progression[progIx]
    noteName = chords[chordName][partIx]
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

    

display.show(Image.PACMAN, wait=False)
radio.on()

while True:
    playNextNote()

    if button_a.was_pressed():
        incPartIx(-1)

    if button_b.was_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        microbit.panic(0) #shut it up!  Require a restart.
