"""
NOTEPADAI
(Microphone)

Sends microphone input to the processor, for testing purposes
"""


from transcription.processor import *

import pyaudio
import sys

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class Microphone:
    def __init__(self):
        self.isRunning = False

        print("Setting up audio stream")
        p = pyaudio.PyAudio()
        self.mic = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

        # Initialise a new Processor object used in .start()
        self.processor = Processor()
        print("Set up")

    # Sends the audio stream from the microphone to the Processor object
    # and prints the result
    def start(self):
        try:
            self.isRunning = True
            for data in self.processor.process(self.__generator__(stream=self.mic)):
                print(data)
        except KeyboardInterrupt:
            self.isRunning = False
            sys.exit(0)

    # transforms a stream of audio data into a stream of gRPC Samples
    # (which are used by the processor, so Microphone and Server can be changed interchangeably)
    def __generator__(self, stream):
        while self.isRunning:
            yield stream.read(CHUNK)
