import RPi.GPIO
import sys
import random
sys.path.append("../../")
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306
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


lcd_oled = SSD1306(128, 64, SPI())
lcd_oled.rotation = 90
lcd_oled.init()
lcd_oled.auto_flush = False

x, y = lcd_oled.width // 2, lcd_oled.height // 2
lcd_oled.draw_circle(x, y, 31)
lcd_oled.draw_circle(x-12, y-10, 7)
lcd_oled.draw_circle(x+12, y-10, 7)
lcd_oled.draw_arc(x, y, 20, 45, 135)
lcd_oled.draw_line(x, y-5, x-4, y+6)
lcd_oled.draw_line(x, y-5, x+4, y+6)
lcd_oled.draw_arc(x, y+3, 5, 45, 135)

lcd_oled.fill_rect(0, 0, 10, 10)

lcd_oled.flush(True)
