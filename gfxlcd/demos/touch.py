import RPi.GPIO
import sys
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
from gfxlcd.driver.ad7843.ad7853 import AD7843
RPi.GPIO.setmode(RPi.GPIO.BCM)


# lcd_tft = ILI9325(240, 320, ILIGPIO())
# lcd_tft.init()


touch = AD7843(240, 320)

while True:
    try:
        ret = touch.get_position()
        if ret:
            # s.draw_pixel(ret[0], ret[1])
            print(ret[0], ret[1])

    except KeyboardInterrupt:
        touch.close()
