import RPi.GPIO
import sys
sys.path.append("../../")
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450
RPi.GPIO.setmode(RPi.GPIO.BCM)

lcd = NJU6450(122, 32, GPIO())
lcd.rotation = 270
lcd.init()
lcd.auto_flush = False

x, y = lcd.width // 2, lcd.height // 2

lcd.draw_pixel(3,1)
lcd.draw_circle(x, y, 15)
lcd.draw_circle(x-7, y-5, 3)
lcd.draw_circle(x+7, y-5, 3)
lcd.draw_arc(x, y, 10, 45, 135)
lcd.draw_line(x, y-3, x-3, y+2)
lcd.draw_line(x, y-3, x+3, y+2)
lcd.draw_arc(x, y, 3, 45, 135)

lcd.fill_rect(0, 0, 5, 10)

lcd.flush(True)
