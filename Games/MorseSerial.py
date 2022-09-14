"""
This module handles the serial communication between the arduino and the python programs.
"""

import serial

class MorseSerial(serial.Serial):
    """
    Handles the serial communication with the arduino encoder/decoder
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def receive(self):
        """ Tries to read a caracter from the serial port, if there isn't one returns None """
        if self.inWaiting():
            return self.read(1).decode()

        return None
