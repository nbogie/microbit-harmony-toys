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
    'iv': ["F3", "Ab4", "C5", "E5"], 
    'V': ["G3", "B4", "D5", "F5"], 
    'v': ["G3", "Bb4", "D5", "F5"], 
    'vi': ["A3", "C5", "E5", "G5"], 
    'VI': ["A3", "C#5", "E5", "G5"], 
    'vii': ["B3", "D5", "F5", "A5"]
}

scale = "C D E F G A B".split(' ')

def assertEq(a, b):
    if a!=b:
        display.scroll("AF." + str(a) + " != " + str(b));
        microbit.panic(1)

def noteOf(noteWord):
    #TODO: consider also flats and sharps
    return noteWord[0]

def octaveOf(noteWord):
    if (noteWord[0] == 'R'):
        return ''
    return int(noteWord.replace('#', "").replace('b', '')[1])
    

def neighbour(note, octave, offset):
    if offset == 0:
        return note + str(octave)

    foundIx = scale.index(note)
    nIx = foundIx + offset
    if nIx >= len(scale):
        nIx = nIx - len(scale)
        octave = octave + 1
    if nIx < 0:
        nIx = nIx + len(scale)
        octave = octave - 1

    return scale[nIx] + str(octave)

    
assertEq(3, octaveOf("B3:1"))
assertEq(5, octaveOf("C#5:1"))
assertEq('C', noteOf("C#5:1"))
assertEq('C', noteOf("C5:1"))

assertEq('G3', neighbour('A', 3, -1))
assertEq('B3', neighbour('A', 3, 1))


neighbourOffset = 0
beatIx = 0
partIx = 1
chordName = '' #received from master

def playNextNote():
    global beatIx
    if (beatIx >= 16):
        beatIx = 0
    noteName = chords[chordName][partIx]
    if (beatIx != 0 and random.random() > 0.9):
        noteName = "R"
    elif neighbourOffset != 0:
        noteName = neighbour(noteOf(noteName), octaveOf(noteName), neighbourOffset)
    music.play(noteName + ":1")
    beatIx = beatIx + 1

def incPartIx(offset):
    global partIx
    partIx = partIx + offset
    if (partIx > 3):
        partIx = 0
    if (partIx < 0):
        partIx = 3


def neighbourOffsetFromGesture():
    #gesture = accelerometer.current_gesture()
    global neighbourOffset
    tilt = accelerometer.get_x()

    if tilt < 20:
        neighbourOffset = -1
    elif tilt > 20:
        neighbourOffset = 1
    else:
        neighbourOffset = 0;



radio.on()
display.show(Image.GHOST, wait=False)
while True:

    msg = radio.receive()
    if (msg != None):
        chordName = msg
        display.scroll(chordName, delay=70, wait=False, loop=False, monospace=False)

    #neighbourOffsetFromGesture()    

    if (chordName != None and chordName != ''):
        playNextNote()

    if button_a.was_pressed():
        incPartIx(-1)

    if button_b.was_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        microbit.panic(0) #shut it up!  Require a restart.
