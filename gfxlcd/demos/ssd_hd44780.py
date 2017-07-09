import sys
sys.path.append("../../")
import RPi.GPIO # NOQA pylint: disable=I0011,F0401
from charlcd.buffered import CharLCD # NOQA
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306
from gfxlcd.driver.hd44780 import HD44780
RPi.GPIO.setmode(RPi.GPIO.BCM)


def test1():
    """demo """
    lcd = SSD1306(128, 64, SPI())

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
