import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306
RPi.GPIO.setmode(RPi.GPIO.BCM)

lcd_oled = SSD1306(128, 64, SPI())
lcd_oled.init()
lcd_oled.auto_flush = False

image_file = Image.open("assets/dsp2017_101_64.png")

lcd_oled.threshold = 50

lcd_oled.threshold = 0
# lcd_oled.transparency_color = [110, 57] #110 #[110, 57]
# lcd_oled.threshold = 255

lcd_oled.draw_image(10, 0, image_file)

lcd_oled.flush(True)
