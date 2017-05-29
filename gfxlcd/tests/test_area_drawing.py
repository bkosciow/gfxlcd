import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.null.null_area import NullArea
from gfxlcd.driver.null.area_driver import AreaDriver


class TestPageDrawing(object):
    def setUp(self):
        self.drv = AreaDriver(10, 16)
        self.lcd = NullArea(10, 16, self.drv, False)
        self.lcd.init()

    def get_buffer(self):
        return [[0] * 16 for x in range(10)]

    def test_has_correct_size(self):
        assert_equal(self.lcd.width, 10)
        assert_equal(self.lcd.height, 16)

    def test_empty_buffer_after_init(self):
        assert_equal(self.drv.buffer, self.get_buffer())

    def test_draw_pixel(self):
        self.lcd.draw_pixel(1, 1)
        buffer = self.get_buffer()
        buffer[1][1] = 1
        assert_equal(self.drv.buffer, buffer)
