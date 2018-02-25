import sys
sys.path.append("../../")
import RPi.GPIO # NOQA pylint: disable=I0011,F0401
from charlcd.buffered import CharLCD # NOQA
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450
from gfxlcd.driver.hd44780 import HD44780
RPi.GPIO.setmode(RPi.GPIO.BCM)


def test1():
    """demo """
    lcd = NJU6450(122, 32, GPIO())

    drv = HD44780(lcd, True)
    print(drv.width, drv.height)
    lcd = CharLCD(drv.width, drv.height, drv, 0, 0)
    lcd.init()
    lcd.write('First Line')
    lcd.write(' it is not', 0, 0)

    lcd.write('HD44780', 6, 3)
    lcd.flush()
    lcd.write('/* ', 12, 0)
    lcd.write('|*|', 12, 1)
    lcd.write(' */', 12, 2)
    lcd.flush()

test1()
