import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.sh1106.spi import SPI
from gfxlcd.driver.sh1106.sh1106 import SH1106
RPi.GPIO.setmode(RPi.GPIO.BCM)


def transform_ij(lcd, i, j):
    offset_width = lcd.height // 2
    if 0 <= i < offset_width:
        i = i + offset_width
    else:
        i = i - offset_width

    return (i,j)


# lcd_oled = SH1106(132, 64, SPI())
lcd_oled = SH1106(132, 64, SPI(CS=21))
lcd_oled.rotation = 270
lcd_oled.xy_callback = transform_ij

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


image_file = Image.open("assets/20x20.png")
lcd_oled.threshold = 0

lcd_oled.draw_image(0, 0, image_file)

lcd_oled.flush(True)
