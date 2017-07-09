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

from gfxlcd.driver.ili9325.gpio import GPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325


class TestILI9325Drawing(object):
    def test_initialize(self):
        drv = GPIO()
        drv.pins['LED'] = 6
        drv.pins['CS'] = 18
        ILI9325(240, 320, drv)



