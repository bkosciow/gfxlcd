import random
import sys
sys.path.append("../../")
from gfxlcd.driver.sh1106.spi import SPI
from gfxlcd.driver.sh1106.sh1106 import SH1106


def hole(x, y):
    lcd_oled.draw_pixel(x+1, y)
    lcd_oled.draw_pixel(x+2, y)
    lcd_oled.draw_pixel(x+3, y)
    lcd_oled.draw_pixel(x+1, y + 4)
    lcd_oled.draw_pixel(x+2, y + 4)
    lcd_oled.draw_pixel(x+3, y + 4)
    lcd_oled.draw_pixel(x, y + 1)
    lcd_oled.draw_pixel(x+4, y + 1)
    lcd_oled.draw_pixel(x, y + 2)
    lcd_oled.draw_pixel(x+4, y + 2)
    lcd_oled.draw_pixel(x, y + 3)
    lcd_oled.draw_pixel(x+4, y + 3)


drv = SPI()
lcd_oled = SH1106(132, 64, drv)

lcd_oled.init()
lcd_oled.auto_flush = False
# for _ in range(0, 50):
#     hole(random.randint(2, 120), random.randint(2, 56))
#
# hole(5, 5)

lcd_oled.draw_line(0,0,lcd_oled.width-1,0)
lcd_oled.draw_line(lcd_oled.width-1,0,lcd_oled.width-1,lcd_oled.height-1)
lcd_oled.draw_line(0,lcd_oled.height-1,lcd_oled.width-1,lcd_oled.height-1)
lcd_oled.draw_line(0,0,0,lcd_oled.height-1)

lcd_oled.draw_line(3,0,3,lcd_oled.height-1)

# hole(15, 13)
# hole(18, 23)
# hole(40, 10)
# o.fill_rect(0,0,5,5)
# o.fill_rect(5,10,15,15)
lcd_oled.flush(True)
