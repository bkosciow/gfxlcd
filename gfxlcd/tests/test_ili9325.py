import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325


class TestILI9325Drawing(object):
    def test_initialize(self):
        drv = GPIO()
        drv.pins['LED'] = 6
        drv.pins['CS'] = 18
        ILI9325(240, 320, drv)
