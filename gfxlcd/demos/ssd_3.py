import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306
RPi.GPIO.setmode(RPi.GPIO.BCM)

lcd_oled = SSD1306(128, 64, SPI())
lcd_oled.rotation = 270
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

# lcd_oled.fill_rect(0, 0, 10, 10)
image_file = Image.open("assets/20x20.png")
lcd_oled.threshold = 0

lcd_oled.draw_image(0, 0, image_file)

lcd_oled.flush(True)
