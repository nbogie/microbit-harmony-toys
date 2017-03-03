from microbit import *
import radio
import random
import music
#Devices with this program will establish a singing order, 
#and take it in turns to sing the next note of a series.
#Start things off with ONE press of button A once all are booted up.

#How it works:
# on waking: 
#   a device generates a random id for itself (we hope there are no duplicates)
#   a device broadcasts that id, in a message: AWAKE <id>
# on receiving AWAKE <otherId>
#   a device will clear its list of known devices, 
#   and reply with its presence: HERE <id>
# on receiving HERE <otherId>
#   a device will add the otherId to its list of ids.
# on receiving a note-play: <scaleDegree> <otherId>
#   a device finds the position of the otherId in its sorted list of all known device ids
#   if device's OWN id is next in numerical order after the one that just played
#     play, and broadcast the play.
#   else
#     do nothing - it's not our turn


def curwenSign(sd):
    images = [
        Image(
        "00000:"
        "79999:"
        "99639:"
        "59659:"
        "02980"
        )
        , Image(
        "00009:"
        "00090:"
        "00900:"
        "09000:"
        "90000"
        )
        , Image(
        "00000:"
        "00000:"
        "99999:"
        "00000:"
        "00000"
        )
        , Image(
        "99997:"
        "99997:"
        "99997:"
        "97000:"
        "97000"
        )
        , Image(
        "00000:"
        "99800:"
        "99984:"
        "99999:"
        "99972"
        )
        , Image(
        "00000:"
        "99990:"
        "09094:"
        "05009:"
        "00007"
        )
        , Image(
        "00099:"
        "00900:"
        "69600:"
        "95960:"
        "99600"
        )]
    return images[sd]
    
def voiceSing(scaleDegree):
    noteName = "C D E F G A B".split(' ')[scaleDegree % 7]
    octave = 3 + scaleDegree/7
    music.play(noteName + str(octave) + ":4")
    
def singThenTell(sd):
    display.show(curwenSign(sd % 7), wait=False)
    voiceSing(sd)
    radio.send(str(sd) + " " + str(myId))
    
def whoIsNextAfter(other):
    global ids
    if (other not in ids):
        ids.add(other)    
    idsList = sorted(ids)
    ix = idsList.index(other)
    if (ix >= len(idsList) - 1):
        ix = 0
    else:
        ix = ix + 1    
    return idsList[ix]

def iAmNextAfter(other):    
    return myId == whoIsNextAfter(other)    
    
def getSenderId(msg):
    return int(msg.split(' ')[1])

def mainLoop():
    global ids, myId
    currentScaleDegree = 0;
    
    while True:
        
        if button_a.was_pressed():
            currentScaleDegree = 0
            singThenTell(currentScaleDegree)
        
        msg = radio.receive()
        if (msg != None):
            if (msg.startswith('AWAKE')):
                senderId = getSenderId(msg)
                ids = set([myId, senderId]) #restart the list
                radio.send('HERE ' + str(myId))
                display.scroll('Rx:Awake', delay=70, wait=False)
            elif (msg.startswith('HERE')):
                senderId = getSenderId(msg)
                ids.add(int(senderId))
                display.scroll("count: " + str(len(ids)), delay=70, wait=False)
            else:
                senderId = getSenderId(msg)
                if (iAmNextAfter(senderId)): # or len(ids) is just one...
                    prev = int(msg.split(' ')[0])
                    currentScaleDegree = (prev + 1) % 14
                    singThenTell(currentScaleDegree)
                else: 
                    display.show(Image.ASLEEP, wait=False) #not my turn...

myId = random.randint(0, 1000000)
ids = set([myId])
radio.config(channel=30, group=30)
radio.on()
radio.send("AWAKE "+str(myId))
mainLoop()
