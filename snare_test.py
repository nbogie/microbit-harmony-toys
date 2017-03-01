from microbit import display, sleep, button_a, button_b
import audio
import random

class Snare:
    """docstring for Snare"""
    def __init__(self):
        self.frame = audio.AudioFrame()

    def make_noise_frame(self, amp):
        #a list of 32 samples each of which is a signed byte (whole number between -128 and 127).
        for i in range(len(self.frame)):
            delta = random.randint(-amp, amp)
            v = 128
            self.frame[i] = v + delta
        return self.frame
    
    def noise_generator(self, count):
        for i in range(count):
            f = self.make_noise_frame(int(40*(count-i)/count))
            yield f
    
    def play_snare(self, duration=20):
        audio.play(self.noise_generator(duration),wait=False)
    
snare = Snare()

while True:
    if button_a.was_pressed():
        snare.play_snare()
