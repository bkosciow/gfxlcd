"""SPI+GPIO connection driver for SSD1306"""
import time
import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO as GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.driver import Driver
GPIO.setmode(GPIO.BCM)


class SPI(Driver):
    """SPI driver"""
    def __init__(self, RST=13, DC=6, CS=None):
        self.pins = {
            'RST': RST,
            'DC': DC,
            'CS': CS,
        }
        self.spi = None

    def init(self):
        """init sequence"""
        for pin in self.pins:
            if self.pins[pin]:
                GPIO.setup(self.pins[pin], GPIO.OUT)
                if pin == 'CS':
                    GPIO.output(self.pins[pin], 1)
                else:
                    GPIO.output(self.pins[pin], 0)

        if not self.spi:
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
        if self.pins['CS']:
            GPIO.output(self.pins['CS'], 0)
        GPIO.output(self.pins['DC'], 0)
        self.spi.xfer2([data])
        if self.pins['CS']:
            GPIO.output(self.pins['CS'], 1)

    def data(self, data, enable=None):
        """send data to device"""
        if self.pins['CS']:
            GPIO.output(self.pins['CS'], 0)
        GPIO.output(self.pins['DC'], 1)
        self.spi.xfer2([data])
        GPIO.output(self.pins['DC'], 0)
        if self.pins['CS']:
            GPIO.output(self.pins['CS'], 1)
