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
radio.on()

def play():
    radio.send(str(ix))
    music.play(chords[ix])


while True:
    if button_a.is_pressed(): 
        ix = ix - 1;
        if (ix < 0):
            ix = 6;
        display.show(str(ix + 1));
        play()       

    if button_b.is_pressed():
        ix = ix + 1;
        if (ix > 6):
            ix = 0;
        display.show(str(ix + 1));
        play()
    

