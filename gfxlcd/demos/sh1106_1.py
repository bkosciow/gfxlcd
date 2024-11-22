import RPi.GPIO
import sys
import random
sys.path.append("../../")
from gfxlcd.driver.sh1106.spi import SPI
from gfxlcd.driver.sh1106.sh1106 import SH1106
RPi.GPIO.setmode(RPi.GPIO.BCM)


def hole(o, x, y):
    o.draw_pixel(x+1, y)
    o.draw_pixel(x+2, y)
    o.draw_pixel(x+3, y)
    o.draw_pixel(x+1, y + 4)
    o.draw_pixel(x+2, y + 4)
    o.draw_pixel(x+3, y + 4)
    o.draw_pixel(x, y + 1)
    o.draw_pixel(x+4, y + 1)
    o.draw_pixel(x, y + 2)
    o.draw_pixel(x+4, y + 2)
    o.draw_pixel(x, y + 3)
    o.draw_pixel(x+4, y + 3)


def draw_points(o):
    for _ in range(0, 50):
        hole(o,
             random.randint(2, o.width - 10),
             random.randint(2, o.height - 10)
        )


def draw_net(o):
    s = 0
    while s < o.width-1:
        o.draw_line(s, 0, s, o.height-1)
        s += 10
    s = 0
    while s < o.height-1:
        o.draw_line(0, s, o.width-1, s)
        s += 10


lcd_oled = SH1106(132, 64, SPI())
lcd_oled.init()
lcd_oled.auto_flush = False

# lcd_oled.fill_rect(0,0,131,63)
# draw_net(lcd_oled)
lcd_oled.draw_line(0,0,lcd_oled.width-1,0)
lcd_oled.draw_line(lcd_oled.width-1,0,lcd_oled.width-1,lcd_oled.height-1)
lcd_oled.draw_line(0,lcd_oled.height-1,lcd_oled.width-1,lcd_oled.height-1)
lcd_oled.draw_line(0,0,0,lcd_oled.height-1)

lcd_oled.draw_line(3,0,3,lcd_oled.height-1)
lcd_oled.draw_rect(4,0,10,10)

lcd_oled.flush(True)
