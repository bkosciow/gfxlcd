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


lcd_oled = SH1106(136, 64, SPI())
lcd_oled.init()
lcd_oled.auto_flush = False

lcd_oled.draw_circle(31, 32, 31)
lcd_oled.draw_circle(19, 22, 7)
lcd_oled.draw_circle(43, 22, 7)
lcd_oled.draw_arc(31, 32, 20, 45, 135)
lcd_oled.draw_line(31, 27, 27, 38)
lcd_oled.draw_line(31, 27, 35, 38)
lcd_oled.draw_arc(31, 35, 5, 45, 135)

lcd_oled.fill_rect(95, 4, 105, 10)
lcd_oled.draw_rect(80, 10, 120, 25)
lcd_oled.fill_rect(80, 26, 120, 59)

lcd_oled.flush(True)
