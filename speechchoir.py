from microbit import *
import music
import radio
import random
import speech

def randomVoice():
    return {'mouth': random.randint(0,255), 'throat': random.randint(0,255)}

myVoice = randomVoice()

def voiceSing(phoneme):
    speech.sing(phoneme, throat=myVoice['throat'], mouth=myVoice['mouth'])
    
def masterLoop():
    while True:
        global myVoice, lastPhoneme
        if button_a.was_pressed():
            phoneme = random.choice(solfa())
            lastPhoneme=phoneme
            voiceSing(phoneme)
            radio.send(phoneme)
            display.scroll(phoneme, delay=70, wait=False, loop=True, monospace=False)
        if button_b.was_pressed():
            myVoice = randomVoice()
            voiceSing(lastPhoneme)

        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll("exit", wait=True)
            break

def slaveLoop():
    global myVoice, lastPhoneme
    while True:
        msg = radio.receive()
        if (msg != None):
            phoneme = msg
            display.scroll(phoneme, delay=70, wait=False, loop=True, monospace=False)
            voiceSing(phoneme)
            lastPhoneme=phoneme
        if button_b.was_pressed():
            myVoice = randomVoice()
            voiceSing(lastPhoneme)


def solfa():
    return [
    "#115DOWWWWWW",   # Doh
    "#103REYYYYYY",   # Re
    "#94MIYYYYYY",    # Mi
    "#88FAOAOAOAOR",  # Fa
    "#78SOHWWWWW",    # Soh
    "#70LAOAOAOAOR",  # La
    "#62TIYYYYYY",    # Ti
    "#58DOWWWWWW",    # Doh
    ]

def doremi():    
    song = ''.join(solfa())
    s = random.randint(15,50)
    display.scroll("s:"+str(s), wait=False, loop=True)
    #speech.sing(song, speed=s, mouth=random.randint(0,255), throat=random.randint(0,255))
    speech.sing(random.choice(solfa())+" " + randomWord(), speed=s, mouth=random.randint(0,255), throat=random.randint(0,255))

lastPhoneme=solfa()[0]

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
