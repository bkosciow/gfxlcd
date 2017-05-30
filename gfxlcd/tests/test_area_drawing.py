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

    def test_draw_two_pixel(self):
        self.lcd.draw_pixel(1, 1)
        self.lcd.draw_pixel(2, 2)
        buffer = self.get_buffer()
        buffer[1][1] = 1
        buffer[2][2] = 1
        assert_equal(self.drv.buffer, buffer)

    def test_draw_horizontal_line(self):
        self.lcd.draw_line(1, 1, 8, 1)
        buffer = self.get_buffer()
        buffer[1][1] = 1
        buffer[2][1] = 1
        buffer[3][1] = 1
        buffer[4][1] = 1
        buffer[5][1] = 1
        buffer[6][1] = 1
        buffer[7][1] = 1
        buffer[8][1] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_vertical_line(self):
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][1] = 1
        buffer[1][2] = 1
        buffer[1][3] = 1
        buffer[1][4] = 1
        buffer[1][5] = 1
        buffer[1][6] = 1
        buffer[1][7] = 1
        buffer[1][8] = 1
        buffer[1][9] = 1
        buffer[1][10] = 1
        buffer[1][11] = 1
        buffer[1][12] = 1
        buffer[1][13] = 1
        buffer[1][14] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_overlapping_lines(self):
        self.lcd.draw_line(1, 1, 8, 1)
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][1] = 1
        buffer[2][1] = 1
        buffer[3][1] = 1
        buffer[4][1] = 1
        buffer[5][1] = 1
        buffer[6][1] = 1
        buffer[7][1] = 1
        buffer[8][1] = 1
        buffer[1][1] = 1
        buffer[1][2] = 1
        buffer[1][3] = 1
        buffer[1][4] = 1
        buffer[1][5] = 1
        buffer[1][6] = 1
        buffer[1][7] = 1
        buffer[1][8] = 1
        buffer[1][9] = 1
        buffer[1][10] = 1
        buffer[1][11] = 1
        buffer[1][12] = 1
        buffer[1][13] = 1
        buffer[1][14] = 1
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line(self):
        self.lcd.draw_line(0, 0, 9, 1)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 1
        buffer[2][0] = 1
        buffer[3][0] = 1
        buffer[4][0] = 1
        buffer[5][1] = 1
        buffer[6][1] = 1
        buffer[7][1] = 1
        buffer[8][1] = 1
        buffer[9][1] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps(self):
        self.lcd.draw_line(0, 0, 9, 15)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][1] = 1
        buffer[2][2] = 1
        buffer[2][3] = 1
        buffer[3][4] = 1
        buffer[3][5] = 1
        buffer[4][6] = 1
        buffer[4][7] = 1
        buffer[5][8] = 1
        buffer[5][9] = 1
        buffer[6][10] = 1
        buffer[6][11] = 1
        buffer[7][12] = 1
        buffer[7][13] = 1
        buffer[8][14] = 1
        buffer[9][15] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 5)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][1] = 1
        buffer[2][1] = 1
        buffer[3][2] = 1
        buffer[4][2] = 1
        buffer[5][3] = 1
        buffer[6][3] = 1
        buffer[7][4] = 1
        buffer[8][4] = 1
        buffer[9][5] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_odd_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 6)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][1] = 1
        buffer[2][2] = 1
        buffer[3][2] = 1
        buffer[4][3] = 1
        buffer[5][3] = 1
        buffer[6][4] = 1
        buffer[7][4] = 1
        buffer[8][5] = 1
        buffer[9][6] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps_odd_rest(self):
        self.lcd.draw_line(0, 0, 8, 6)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][1] = 1
        buffer[2][2] = 1
        buffer[3][3] = 1
        buffer[4][3] = 1
        buffer[5][3] = 1
        buffer[6][4] = 1
        buffer[7][5] = 1
        buffer[8][6] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def test_draw_rect(self):
        self.lcd.draw_rect(2, 2, 7, 11)
        buffer = self.get_buffer()
        buffer[2][2] = 1
        buffer[2][3] = 1
        buffer[2][4] = 1
        buffer[2][5] = 1
        buffer[2][6] = 1
        buffer[2][7] = 1
        buffer[2][8] = 1
        buffer[2][9] = 1
        buffer[2][10] = 1
        buffer[2][11] = 1
        buffer[7][2] = 1
        buffer[7][3] = 1
        buffer[7][4] = 1
        buffer[7][5] = 1
        buffer[7][6] = 1
        buffer[7][7] = 1
        buffer[7][8] = 1
        buffer[7][9] = 1
        buffer[7][10] = 1
        buffer[7][11] = 1

        buffer[3][2] = 1
        buffer[4][2] = 1
        buffer[5][2] = 1
        buffer[6][2] = 1
        buffer[3][11] = 1
        buffer[4][11] = 1
        buffer[5][11] = 1
        buffer[6][11] = 1
        self.draw_buffer(self.drv.buffer)
        assert_equal(self.drv.buffer, buffer)

    def draw_buffer(self, buffer):
        for y in range(self.lcd.height):
            row = ""
            for x in range(self.lcd.width):
                row += str(buffer[x][y])
            print (row)
