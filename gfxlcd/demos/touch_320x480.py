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

touch = XPT2046(320, 480, 17, callback, 7)
# touch.correction = {
#     'x': 1,#3394,#364,
#     'y': 1,#3350,#430,
#     'ratio_x': 1,
#     'ratio_y': 1
# }
touch.init()

while True:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        touch.close()
        # RPi.GPIO.cleanup()

