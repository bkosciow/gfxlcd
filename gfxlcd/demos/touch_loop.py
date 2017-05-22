import RPi.GPIO
import sys
import time
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
from gfxlcd.driver.xpt2046.xpt2046 import XPT2046
from gfxlcd.driver.ad7843.ad7843 import AD7843
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486
RPi.GPIO.setmode(RPi.GPIO.BCM)


# lcd_tft = ILI9325(240, 320, ILIGPIO())
# lcd_tft.init()
lcd_tft = ILI9486(320, 480, SPI())
lcd_tft.init()

def callback(position):
    print('(x,y)', position)

#touch = AD7843(240, 320)
touch = XPT2046(320, 480)

touch.init()

while True:
    try:
        time.sleep(0.05)
        ret = touch.get_position()
        if ret:
            print(ret[0], ret[1])

    except KeyboardInterrupt:
        touch.close()
        RPi.GPIO.cleanup()

