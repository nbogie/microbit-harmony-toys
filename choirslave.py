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
ix = 0;

def play():
    y = chords[ix][:]
    y.reverse()
    music.play(y)

radio.on()
display.show(Image.GHOST)

while True:
    msg = radio.receive()
    if (msg != None):
        display.show(msg)
        ix = int(msg)
        play()      
