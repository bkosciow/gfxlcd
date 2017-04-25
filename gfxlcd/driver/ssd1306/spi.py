"""SPI+GPIO connection driver for SSD1306"""
import time
import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO as GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.driver import Driver
GPIO.setmode(GPIO.BCM)


class SPI(Driver):
    """SPI driver"""
    def __init__(self):
        self.pins = {
            'RST': 13,
            'DC': 6,
        }
        self.spi = None

    def init(self):
        """init sequence"""
        for pin in self.pins:
            GPIO.setup(self.pins[pin], GPIO.OUT)
            GPIO.output(self.pins[pin], 0)

        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 8000000
        spi.mode = 0
        self.spi = spi

    def reset(self):
        """reset device"""
        GPIO.output(self.pins['RST'], 1)
        time.sleep(0.025)
        GPIO.output(self.pins['RST'], 0)
        time.sleep(0.025)
        GPIO.output(self.pins['RST'], 1)
        time.sleep(0.025)

    def cmd(self, data, enable=None):
        """send command to device"""
        GPIO.output(self.pins['DC'], 0)
        self.spi.xfer2([data])

    def data(self, data, enable=None):
        """send data to device"""
        GPIO.output(self.pins['DC'], 1)
        self.spi.xfer2([data])
        GPIO.output(self.pins['DC'], 0)
