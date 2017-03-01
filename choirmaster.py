from microbit import *
import music
import radio
import random
import microbit

#TODO: remember and repeat the randomly generated ostinato
#TODO: R + 10th is nice
#TODO: 3 + 5 is nice (rootless)
#TODO: persist a programmed chord progression
chordIndex = 'I ii II iii III IV iv V v vi VI vii'.split(' ')
silent = False

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
progressions = [ "vi V I IV".split(' '),
                 "I III IV VI ii VI V".split(' '), 
                 "vi IV vi IV V iii".split(' '),
                 "I III IV iv I ii II V".split(' ')
]

progression = progressions[3]
partIx = 0


def incProgIx():
    global progIx
    progIx = progIx + 1
    if (progIx >= len(progression)):
        progIx = 0;    
    chordName = progression[progIx]
    #delays things
    #display.show(chordName)
    display.scroll(chordName, delay=70, wait=False, loop=False, monospace=False)

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

    
class EditMode:
    def __init__(self):
        self.chordIx = 0
        self.chords = []
        self.chordName = chordIndex[self.chordIx]

    def incChord(self):
        global chordIndex
        self.chordIx = self.chordIx + 1
        if self.chordIx >= len(chordIndex):
            self.chordIx = 0
        self.chordName = chordIndex[self.chordIx]
        self.display()
    
    def lockChord(self):
        self.chords.append(self.chordName)
        display.scroll(",".join(self.chords), wait=True, delay=70)

    def finaliseProgression(self):
        global progression
        progression = self.chords
        display.show(Image.YES, wait=True)

    def display(self):
        display.scroll(self.chordName, wait=False, delay=70)

if button_a.is_pressed():
    editor = EditMode()
    display.scroll("Editing...", wait=True, delay=50)
    editor.display()

    while True:
        if button_a.is_pressed() and button_b.is_pressed():
            editor.finaliseProgression()
            break

        if button_a.was_pressed():
            editor.incChord()

        if button_b.was_pressed():
            editor.lockChord()


display.show(Image.PACMAN, wait=False)
radio.on()

def toggleSilence():
    global silent
    silent = not silent
    sleep(300)
    display.show(Image.ASLEEP if silent else Image.MUSIC_QUAVERS)
    
while True:
    if not silent:
        playNextNote()

    if button_a.was_pressed():
        incPartIx(-1)

    if button_b.was_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        toggleSilence()
