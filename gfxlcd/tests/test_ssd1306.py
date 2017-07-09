import sys
sys.path.append("../../")
from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306


class TestNJU6450(object):
    def test_initialize(self):
        SSD1306(128, 64, SPI())
