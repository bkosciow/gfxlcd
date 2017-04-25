"""NJU6450 gpio driver class"""
import time
import RPi.GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.driver import Driver

RPi.GPIO.setmode(RPi.GPIO.BCM)


class GPIO(Driver):
    """GPIO driver"""
    def __init__(self):
        self.pins = {
            'A0': 17,
            'E1': 22,
            'E2': 21,
            'D0': 23,
            'D1': 24,
            'D2': 25,
            'D3': 12,
            'D4': 16,
            'D5': 20,
            'D6': 26,
            'D7': 19,
            'RST': 5,
        }

        self.data_pins = [
            'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'
        ]

    def init(self):
        """init a device"""
        for pin in self.pins:
            RPi.GPIO.setup(self.pins[pin], RPi.GPIO.OUT)
            RPi.GPIO.output(self.pins[pin], 0)

    def reset(self):
        """resets a device"""
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.025)
        RPi.GPIO.output(self.pins['RST'], 0)
        time.sleep(0.025)
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.025)
        RPi.GPIO.output(self.pins['A0'], 0)
        RPi.GPIO.output(self.pins['E1'], 1)
        RPi.GPIO.output(self.pins['E2'], 1)

    def cmd(self, data, enable):
        """send command"""
        RPi.GPIO.output(self.pins['A0'], 0)
        self.send(data, enable)

    def data(self, data, enable):
        """send data"""
        RPi.GPIO.output(self.pins['A0'], 1)
        self.send(data, enable)

    def send(self, data, enable):
        """Write to gpio"""
        RPi.GPIO.output(self.pins['E1'], 0)
        RPi.GPIO.output(self.pins['E2'], 0)
        for i in self.data_pins:
            value = data & 0x01
            RPi.GPIO.output(self.pins[i], value)
            data >>= 1

        RPi.GPIO.output(self.pins['E'+str(enable+1)], 1)
        time.sleep(0.00025)
        RPi.GPIO.output(self.pins['E1'], 0)
        RPi.GPIO.output(self.pins['E2'], 0)
