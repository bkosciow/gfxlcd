import sys
sys.path.append("../../")
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450


class TestNJU6450(object):
    def test_initialize(self):
        drv = GPIO()
        NJU6450(122, 32, drv)
