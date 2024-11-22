"""SH1106 chip driver"""
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306


class SH1106(SSD1306):
    def __init__(self, width, height, driver, auto_flush=False):
        SSD1306.__init__(self, width, height, driver, auto_flush)
        self.offset_j = 0
