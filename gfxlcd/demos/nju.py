import random
import sys
sys.path.append("../../")
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450


def hole(x, y):
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


drv = GPIO()
o = NJU6450(122, 32, drv)

o.init()
o.auto_flush = False
for _ in range(0, 50):
    hole(random.randint(2, 115), random.randint(2, 25))
hole(10, 10)
hole(15, 13)
hole(18, 23)
hole(40, 10)
o.flush(True)
