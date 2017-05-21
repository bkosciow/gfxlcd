import RPi.GPIO
import sys
import time
sys.path.append("../../")
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486
from gfxlcd.driver.xpt2046.xpt2046 import XPT2046
RPi.GPIO.setmode(RPi.GPIO.BCM)


lcd_tft = ILI9486(320, 480, SPI())
lcd_tft.init()


def callback(position):
    print('(x,y)', position)

touch = XPT2046(480, 320, 17, callback, 7)
#touch.rotate = 270

touch.init()

while True:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        touch.close()
        # RPi.GPIO.cleanup()

