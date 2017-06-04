__author__ = 'kosci'

import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.null.null_page import NullPage


class TestChip(object):
    def setUp(self):
        self.lcd = NullPage(10, 16, None, False)

    def test_rotate_by_0(self):
        self.lcd.rotation = 0
        assert_equal(10, self.lcd.width)
        assert_equal(16, self.lcd.height)

    def test_rotate_by_90(self):
        self.lcd.rotation = 90
        assert_equal(16, self.lcd.width)
        assert_equal(10, self.lcd.height)

    def test_rotate_by_180(self):
        self.lcd.rotation = 180
        assert_equal(10, self.lcd.width)
        assert_equal(16, self.lcd.height)

    def test_rotate_by_270(self):
        self.lcd.rotation = 270
        assert_equal(16, self.lcd.width)
        assert_equal(10, self.lcd.height)
