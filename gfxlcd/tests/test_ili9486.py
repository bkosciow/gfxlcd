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

from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486


class TestILI9486(object):
    def test_initialize(self):
        ILI9486(320, 480, SPI())
