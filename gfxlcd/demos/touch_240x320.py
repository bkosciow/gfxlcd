import RPi.GPIO
import sys
import time
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
from gfxlcd.driver.ad7843.ad7843 import AD7843
RPi.GPIO.setmode(RPi.GPIO.BCM)


lcd_tft = ILI9325(240, 320, ILIGPIO())
lcd_tft.init()


def callback(position):
    print('(x,y)', position)

touch = AD7843(240, 320, 26, callback)
touch.rotate = 180
touch.init()

while True:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        touch.close()
        # RPi.GPIO.cleanup()

