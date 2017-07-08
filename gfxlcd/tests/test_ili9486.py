import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486


class TestILI9486(object):
    def test_initialize(self):
        ILI9486(320, 480, SPI())
