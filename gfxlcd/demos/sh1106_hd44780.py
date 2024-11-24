import sys
sys.path.append("../../")
import RPi.GPIO # NOQA pylint: disable=I0011,F0401
from charlcd.buffered import CharLCD # NOQA
from gfxlcd.driver.sh1106.spi import SPI
from gfxlcd.driver.sh1106.sh1106 import SH1106
from gfxlcd.driver.hd44780 import HD44780
RPi.GPIO.setmode(RPi.GPIO.BCM)

def transform_ij(lcd, i, j):
    offset_width = lcd.width // 2
    if 0 <= i < offset_width:
        i = i + offset_width
    else:
        i = i - offset_width

    return (i,j)

def test1():
    """demo """
    # lcd = SH1106(132, 64, SPI())
    lcd = SH1106(132, 64, SPI(CS=21))
    lcd.xy_callback = transform_ij
    drv = HD44780(lcd, True)
    print(drv.width, drv.height)
    lcd = CharLCD(drv.width, drv.height, drv, 0, 0)
    lcd.init()
    lcd.write('First')

    lcd.write('HD44780', 6, 3)
    lcd.flush()
    lcd.write('/* ', 12, 0)
    lcd.write('|*|', 12, 1)
    lcd.write(' */', 12, 2)
    lcd.flush()

test1()
