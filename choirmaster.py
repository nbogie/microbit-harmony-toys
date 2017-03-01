from microbit import *
import music
import radio
import random
import microbit

#TODO: remember and repeat the randomly generated ostinato
#TODO: R + 10th is nice
#TODO: 3 + 5 is nice (rootless)
#TODO: persist a programmed chord progression
chordIndex = 'I #Idim ii II iii III IV iv V v vi VI vii'.split(' ')
silent = False

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


progIx = 0
beatIx = 0
progressions = [ "vi V I IV".split(' '),
                 "I III IV VI ii VI V".split(' '), 
                 "vi IV vi IV V iii".split(' '),
                 "I III IV iv I ii II V".split(' '),
                 "I #Idim ii V ii V vi IV".split(' ')
]

progression = progressions[4]
partIx = 0

def incProgIx():
    global progIx
    progIx = progIx + 1
    if (progIx >= len(progression)):
        progIx = 0;    
    chordName = progression[progIx]
    
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
        noteName = "R"
    music.play(noteName + ":1")
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
        display.scroll(",".join(self.chords), wait=False, delay=70)

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
            sleep(1000)
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
    display.show(Image.ASLEEP if silent else Image.MUSIC_QUAVERS, wait=False)
    sleep(1000)

while True:
    if not silent:
        playNextNote()

    if button_a.was_pressed():
        incPartIx(-1)

    if button_b.was_pressed():
        incPartIx(1)

    if button_a.is_pressed() and button_b.is_pressed():
        toggleSilence()
