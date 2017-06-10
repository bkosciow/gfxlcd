import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306
RPi.GPIO.setmode(RPi.GPIO.BCM)

lcd = SSD1306(128, 64, SPI())
lcd.rotation = 0
lcd.init()
lcd.auto_flush = False

lcd.draw_text(25, 1, "Star Wars")
lcd.draw_text(30, 10, "Death Star")

image_file = Image.open("assets/20x20.png")
lcd.threshold = 0

lcd.draw_image(0, 0, image_file)

lcd.flush(True)
