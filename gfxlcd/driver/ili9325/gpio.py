import time
import RPi.GPIO
from gfxlcd.abstract.driver import Driver

RPi.GPIO.setmode(RPi.GPIO.BCM)


class GPIO(Driver):
    def __init__(self):
        self.pins = {
            'RS': 27,
            'W': 17,
            'DB8': 22,
            'DB9': 23,
            'DB10': 24,
            'DB11': 5,
            'DB12': 12,
            'DB13': 16,
            'DB14': 20,
            'DB15': 21,
            'RST': 25,
        }
        self.data_pins = [
            'DB8', 'DB9', 'DB10', 'DB11', 'DB12', 'DB13', 'DB14', 'DB15',
        ]

    def init(self):
        """initialize pins"""
        for pin in self.pins:
            RPi.GPIO.setup(self.pins[pin], RPi.GPIO.OUT)
            RPi.GPIO.output(self.pins[pin], 0)

    def reset(self):
        """reset a display"""
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.005)
        RPi.GPIO.output(self.pins['RST'], 0)
        time.sleep(0.005)
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.005)

    def _set_pins(self, bits):
        """set rpi pins"""
        for pin in self.data_pins:
            value = bits & 0x01
            RPi.GPIO.output(self.pins[pin], value)
            bits >>= 1

    def cmd(self, char, enable):
        """send command to display"""
        RPi.GPIO.output(self.pins['RS'], 0)
        self.send(char, enable)

    def send(self, char, enable):
        """send 16bit as 2*8bit"""
        self._set_pins(char >> 8)
        RPi.GPIO.output(self.pins['W'], 0)
        RPi.GPIO.output(self.pins['W'], 1)
        self._set_pins(char)
        RPi.GPIO.output(self.pins['W'], 0)
        RPi.GPIO.output(self.pins['W'], 1)

    def data(self, data, enable):
        """send data to display"""
        RPi.GPIO.output(self.pins['RS'], 1)
        self.send(data, enable)

    def cmd_data(self, cmd, data):
        RPi.GPIO.output(self.pins['RS'], 0)
        self.send(cmd, None)
        RPi.GPIO.output(self.pins['RS'], 1)
        self.send(data, None)