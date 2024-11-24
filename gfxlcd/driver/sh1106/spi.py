"""SPI+GPIO connection driver for SH1106"""
import RPi.GPIO as GPIO  # pylint: disable=I0011,F0401
from gfxlcd.driver.ssd1306.spi import SPI as BASE_SPI
GPIO.setmode(GPIO.BCM)


class SPI(BASE_SPI):
    pass
