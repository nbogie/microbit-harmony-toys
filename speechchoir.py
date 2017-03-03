from microbit import *
import music
import radio
import random
import speech

#Instructions: Start with button a pressed, to become master.
#              Press A on master to sing a note and tell listening slaves about it.
#                 Listening slaves will sing a harmony to a note.
#              Press A to change a slave's harmony offset.
#              Press B to change voice to a new random one.

pitches = [115, 103, 94, 88, 78, 70, 62, 58, 52, 46, 44, 39, 35, 31, 29, 26, 23, 22]

#return a pitched phoneme string for the given scale degree (count from 0)
#e.g. solfa(0) returns "#115DOWWWWWWW", 
#e.g. solfa(4) returns "#78SOHWWWW"
#This string can then be passed to speech.sing(str)
def solfa(n=None):
    global pitches
    if n == None:
        n = random.randint(0, len(pitches)-1)
        
    phonemes = [
        "DOWWWWWW",   # Doh
        "REYYYYYY",   # Re
        "MIYYYYYY",    # Mi
        "FAOAOAOAOR",  # Fa
        "SOHWWWWW",    # Soh
        "LAOAOAOAOR",  # La
        "TIYYYYYY"    # Ti
    ]
    if n >= len(pitches):
        n = n % 7
    pitch = pitches[n]
    phoneme = phonemes[n % 7]
    return "#{}{}".format(str(pitch), phoneme)

def randomVoice():
    return {'mouth': random.randint(0,255), 'throat': random.randint(0,255)}

#speech.sing  the given phoneme, using my voice
def voiceSing(phoneme):
    speech.sing(phoneme, speed=80, throat=myVoice['throat'], mouth=myVoice['mouth'])
    
def masterLoop():
    lastPhoneme=solfa(0)

    while True:
        global myVoice
        if button_a.was_pressed():
            i = random.randint(0, len(pitches)-6)
            phoneme = solfa(i)
            lastPhoneme=phoneme
            voiceSing(phoneme)
            radio.send(str(i))
            
            display.scroll(phoneme, delay=70, wait=False, loop=True, monospace=False)
        if button_b.was_pressed():
            myVoice = randomVoice()
            voiceSing(lastPhoneme)

        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll("exit", wait=True)
            break

def slaveLoop():
    global myVoice
    lastPhoneme=solfa(0)
    offset = 5 # a sixth above
    
    while True:
        msg = radio.receive()
        if (msg != None):
            i = int(msg)
            phoneme = solfa(i + offset) # sing a harmony above the master

            display.scroll(phoneme, delay=70, wait=False, loop=True, monospace=False)
            voiceSing(phoneme)
            lastPhoneme=phoneme
        if button_b.was_pressed():
            myVoice = randomVoice()
            voiceSing(lastPhoneme)

        if button_a.was_pressed():
            offset = (offset + 1) % 10 #allow up to a 10th above.
            display.scroll(str(offset), wait=False)

myVoice = randomVoice()


isMaster=False

if button_a.is_pressed():
    isMaster=True

chordName = '' #received from master
radio.on()
display.show(Image.PACMAN if isMaster else Image.GHOST, wait=False)

if isMaster:
    masterLoop()
else:
    slaveLoop()
