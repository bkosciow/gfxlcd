"""SPI communication driver"""
import time
import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.driver import Driver
RPi.GPIO.setmode(RPi.GPIO.BCM)


class SPI(Driver):
    """SPI communication driver"""
    def __init__(self, spi=0, speed=1000000):
        self.pins = {
            'CS': 8,
            'RST': 25,
            'RS': 24,
            'LED': None
        }
        self.spi = spidev.SpiDev()
        self.spi.open(spi, 0)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0

    def init(self):
        """initialize pins"""
        for pin in self.pins:
            if self.pins[pin] is not None:
                RPi.GPIO.setup(self.pins[pin], RPi.GPIO.OUT)
                RPi.GPIO.output(self.pins[pin], 0)

        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 1)

        if self.pins['LED']:
            RPi.GPIO.output(self.pins['LED'], 1)

    def reset(self):
        """reset a display"""
        if self.pins['LED']:
            RPi.GPIO.output(self.pins['LED'], 1)
        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 1)
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.005)
        RPi.GPIO.output(self.pins['RST'], 0)
        time.sleep(0.005)
        RPi.GPIO.output(self.pins['RST'], 1)
        time.sleep(0.005)

    def cmd(self, data, enable):
        """send command to display"""
        RPi.GPIO.output(self.pins['RS'], 0)
        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 0)
        self.spi.xfer2([data])
        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 1)

    def data(self, data, enable):
        """send data to display"""
        RPi.GPIO.output(self.pins['RS'], 1)
        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 0)
        self.spi.xfer2([data >> 8, data])
        if self.pins['CS']:
            RPi.GPIO.output(self.pins['CS'], 1)
