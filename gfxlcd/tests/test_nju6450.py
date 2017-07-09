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

from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450


class TestNJU6450(object):
    def test_initialize(self):
        drv = GPIO()
        NJU6450(122, 32, drv)
