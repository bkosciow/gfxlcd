import sys
sys.path.append("../../")
import RPi.GPIO as GPIO  # NOQA pylint: disable=I0011,F0401
from charlcd.buffered import CharLCD # NOQA
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
from gfxlcd.driver.hd44780 import HD44780
GPIO.setmode(GPIO.BCM)


def test1():
    """demo """
    ili_drv = ILIGPIO()
    ili_drv.pins['LED'] = 6
    ili_drv.pins['CS'] = 18
    lcd = ILI9325(240, 320, ili_drv)
    lcd.auto_flush = False
    lcd.rotation = 0

    drv = HD44780(lcd)
    lcd = CharLCD(drv.width, drv.height, drv, 0, 0)
    lcd.init()

    lcd.write('First Line')
    lcd.write("This text is displayed", 2, 18)
    lcd.write("via CharLCD package", 10, 20)
    lcd.write('GfxLCD uses driver', 1, 22)
    lcd.write('to be compatible with', 9, 24)
    lcd.write('HD44780', 10, 26)
    lcd.flush()

    lcd.write('/* ', 19, 0)
    lcd.write('|*|', 19, 1)
    lcd.write(' */', 19, 2)
    lcd.flush()

    lcd.write('BUM', 19, 5)
    lcd.flush()

test1()
