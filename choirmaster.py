from microbit import *
import music
import radio

chords = [
    ["C4:1", "E4:1", "G4:1", "B4:1"], 
    ["D4:1", "F4:1", "A4:1", "C5:1"], 
    ["E4:1", "G4:1", "B4:1", "D5:1"], 
    ["F4:1", "A4:1", "C5:1", "E5:1"], 
    ["G4:1", "B4:1", "D5:1", "F5:1"], 
    ["A4:1", "C5:1", "E5:1", "G5:1"], 
    ["B4:1", "D5:1", "F5:1", "A5:1"]
    ]

progIx = 0
ix = 0
progression = [1,4,5,4]

display.show(Image.PACMAN)
radio.on()

def incProgIx():
    global progIx, ix
    progIx = progIx + 1
    display.show(str(progIx))
    if (progIx >= len(progression)):
        progIx = 0;
    ix = progression[progIx] - 1

    
def play():
    radio.send(str(ix))
    music.play(chords[ix])

def incIx(offset):
    global ix
    ix = ix + offset
    if (ix > 6):
        ix = 0;
    if (ix < 0):
        ix = 6;
    display.show(str(ix + 1));


while True:
    play()
    play()
    play()
    play()
    incProgIx()

    if button_b.is_pressed():
        incProgIx()
        play()