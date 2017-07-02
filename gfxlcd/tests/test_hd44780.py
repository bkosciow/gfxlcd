__author__ = 'kosci'

import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.null.null_page import NullPage
from gfxlcd.driver.hd44780 import HD44780
from charlcd.buffered import CharLCD


class TestChip(object):
    def setUp(self):
        self.gfx_lcd = NullPage(132, 16, None, False)
        self.drv = HD44780(self.gfx_lcd)
        self.output = [" ".ljust(16, " ") for i in range(0, 2)]

    def get_lcd(self):
        lcd = CharLCD(self.drv.width, self.drv.height, self.drv, 0, 0)
        lcd.init()
        return lcd

    def test_get_size_in_chars(self):
        assert_equal(16, self.drv.width)
        assert_equal(2, self.drv.height)

    def test_init_small_hd44780(self):
        lcd = CharLCD(self.drv.width, self.drv.height, self.drv, 0, 0)
        lcd.init()

    def test_write_to_buffer(self):
        lcd = self.get_lcd()
        lcd.write('Hello')
        lcd.write('     world', 0, 1)
        self.output[0] = "Hello" + " ".ljust(11, " ")
        self.output[1] = "     world" + " ".ljust(6, " ")
        assert_equal(lcd.buffer, self.output)

    def test_flush(self):
        lcd = self.get_lcd()
        lcd.write('Hello')
        lcd.write('     world', 0, 1)
        lcd.flush()
