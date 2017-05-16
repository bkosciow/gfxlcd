import sys
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325


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


def draw_net(o):
    s = 0
    while s < o.width-1:
        o.draw_line(s, 0, s, o.height-1)
        s += 10
    s = 0
    while s < o.height-1:
        o.draw_line(0, s, o.width-1, s)
        s += 10


drv = GPIO()
drv.pins['LED'] = 6
drv.pins['CS'] = 18
o = ILI9325(240, 320, drv)

o.init()
# for _ in range(0, 50):
#     hole(random.randint(2,o.width-3), random.randint(2,o.height-3))
#
# draw_net(o)

o.color = (10, 230, 200)
o.draw_circle(60, 15, 15)
o.color = (0, 250, 20)
o.draw_circle(53, 10, 3)
o.draw_circle(67, 10, 3)
o.color = (250, 150, 20)
o.draw_arc(60, 15, 10, 45, 135)
o.color = (10, 230, 200)
o.draw_line(60, 12, 57, 17)
o.draw_line(60, 12, 63, 17)
o.draw_arc(60, 15, 3, 45, 135)

o.background_color = (200, 0, 120)
o.fill_rect(2, 2, 42, 29)
o.background_color = (20, 200, 120)
o.fill_rect(119, 2, 109, 12)
o.fill_rect(119, 17, 109, 19)

o.background_color = (255, 255, 255)
o.fill_rect(77, 6, 105, 16)
o.background_color = (255, 0, 0)
o.fill_rect(77, 16, 105, 25)
