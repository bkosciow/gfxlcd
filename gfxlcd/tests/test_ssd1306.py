import sys
sys.path.append("../../")
from unittest.mock import patch, MagicMock

MockRPi = MagicMock()
MockSpidev = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "spidev": MockSpidev
}

patcher = patch.dict("sys.modules", modules)
patcher.start()

from gfxlcd.driver.ssd1306.spi import SPI
from gfxlcd.driver.ssd1306.ssd1306 import SSD1306


class TestNJU6450(object):
    def test_initialize(self):
        SSD1306(128, 64, SPI())
