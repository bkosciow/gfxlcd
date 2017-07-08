import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.null.null_area import NullArea
from gfxlcd.driver.null.area_driver import AreaDriver


class TestAreaDrawing(object):
    color_black = {'R': 0, 'G': 0, 'B': 0}
    color_white = {'R': 255, 'G': 255, 'B':255}

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
        buffer[1][1] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_two_pixel(self):
        self.lcd.draw_pixel(1, 1)
        self.lcd.draw_pixel(2, 2)
        buffer = self.get_buffer()
        buffer[1][1] = self.color_white
        buffer[2][2] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_horizontal_line(self):
        self.lcd.draw_line(1, 1, 8, 1)
        buffer = self.get_buffer()
        buffer[1][1] = self.color_white
        buffer[2][1] = self.color_white
        buffer[3][1] = self.color_white
        buffer[4][1] = self.color_white
        buffer[5][1] = self.color_white
        buffer[6][1] = self.color_white
        buffer[7][1] = self.color_white
        buffer[8][1] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_vertical_line(self):
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][1] = self.color_white
        buffer[1][2] = self.color_white
        buffer[1][3] = self.color_white
        buffer[1][4] = self.color_white
        buffer[1][5] = self.color_white
        buffer[1][6] = self.color_white
        buffer[1][7] = self.color_white
        buffer[1][8] = self.color_white
        buffer[1][9] = self.color_white
        buffer[1][10] = self.color_white
        buffer[1][11] = self.color_white
        buffer[1][12] = self.color_white
        buffer[1][13] = self.color_white
        buffer[1][14] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_overlapping_lines(self):
        self.lcd.draw_line(1, 1, 8, 1)
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][1] = self.color_white
        buffer[2][1] = self.color_white
        buffer[3][1] = self.color_white
        buffer[4][1] = self.color_white
        buffer[5][1] = self.color_white
        buffer[6][1] = self.color_white
        buffer[7][1] = self.color_white
        buffer[8][1] = self.color_white
        buffer[1][1] = self.color_white
        buffer[1][2] = self.color_white
        buffer[1][3] = self.color_white
        buffer[1][4] = self.color_white
        buffer[1][5] = self.color_white
        buffer[1][6] = self.color_white
        buffer[1][7] = self.color_white
        buffer[1][8] = self.color_white
        buffer[1][9] = self.color_white
        buffer[1][10] = self.color_white
        buffer[1][11] = self.color_white
        buffer[1][12] = self.color_white
        buffer[1][13] = self.color_white
        buffer[1][14] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line(self):
        self.lcd.draw_line(0, 0, 9, 1)
        buffer = self.get_buffer()
        buffer[0][0] = self.color_white
        buffer[1][0] = self.color_white
        buffer[2][0] = self.color_white
        buffer[3][0] = self.color_white
        buffer[4][0] = self.color_white
        buffer[5][1] = self.color_white
        buffer[6][1] = self.color_white
        buffer[7][1] = self.color_white
        buffer[8][1] = self.color_white
        buffer[9][1] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps(self):
        self.lcd.draw_line(0, 0, 9, 15)
        buffer = self.get_buffer()
        buffer[0][0] = self.color_white
        buffer[1][1] = self.color_white
        buffer[2][2] = self.color_white
        buffer[2][3] = self.color_white
        buffer[3][4] = self.color_white
        buffer[3][5] = self.color_white
        buffer[4][6] = self.color_white
        buffer[4][7] = self.color_white
        buffer[5][8] = self.color_white
        buffer[5][9] = self.color_white
        buffer[6][10] = self.color_white
        buffer[6][11] = self.color_white
        buffer[7][12] = self.color_white
        buffer[7][13] = self.color_white
        buffer[8][14] = self.color_white
        buffer[9][15] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 5)
        buffer = self.get_buffer()
        buffer[0][0] = self.color_white
        buffer[1][1] = self.color_white
        buffer[2][1] = self.color_white
        buffer[3][2] = self.color_white
        buffer[4][2] = self.color_white
        buffer[5][3] = self.color_white
        buffer[6][3] = self.color_white
        buffer[7][4] = self.color_white
        buffer[8][4] = self.color_white
        buffer[9][5] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_odd_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 6)
        buffer = self.get_buffer()
        buffer[0][0] = self.color_white
        buffer[1][1] = self.color_white
        buffer[2][2] = self.color_white
        buffer[3][2] = self.color_white
        buffer[4][3] = self.color_white
        buffer[5][3] = self.color_white
        buffer[6][4] = self.color_white
        buffer[7][4] = self.color_white
        buffer[8][5] = self.color_white
        buffer[9][6] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_diagonal_line_even_steps_odd_rest(self):
        self.lcd.draw_line(0, 0, 8, 6)
        buffer = self.get_buffer()
        buffer[0][0] = self.color_white
        buffer[1][1] = self.color_white
        buffer[2][2] = self.color_white
        buffer[3][3] = self.color_white
        buffer[4][3] = self.color_white
        buffer[5][3] = self.color_white
        buffer[6][4] = self.color_white
        buffer[7][5] = self.color_white
        buffer[8][6] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_rect(self):
        self.lcd.draw_rect(2, 2, 7, 11)
        buffer = self.get_buffer()
        buffer[2][2] = self.color_white
        buffer[2][3] = self.color_white
        buffer[2][4] = self.color_white
        buffer[2][5] = self.color_white
        buffer[2][6] = self.color_white
        buffer[2][7] = self.color_white
        buffer[2][8] = self.color_white
        buffer[2][9] = self.color_white
        buffer[2][10] = self.color_white
        buffer[2][11] = self.color_white
        buffer[7][2] = self.color_white
        buffer[7][3] = self.color_white
        buffer[7][4] = self.color_white
        buffer[7][5] = self.color_white
        buffer[7][6] = self.color_white
        buffer[7][7] = self.color_white
        buffer[7][8] = self.color_white
        buffer[7][9] = self.color_white
        buffer[7][10] = self.color_white
        buffer[7][11] = self.color_white

        buffer[3][2] = self.color_white
        buffer[4][2] = self.color_white
        buffer[5][2] = self.color_white
        buffer[6][2] = self.color_white
        buffer[3][11] = self.color_white
        buffer[4][11] = self.color_white
        buffer[5][11] = self.color_white
        buffer[6][11] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_fill_rect(self):
        self.lcd.fill_rect(2, 2, 7, 11)
        buffer = self.get_buffer()
        for x in range(6):
            for y in range(10):
                buffer[2+x][2+y] = self.color_black
        assert_equal(self.drv.buffer, buffer)

    def test_draw_circle(self):
        self.lcd.draw_circle(5, 8, 3)
        buffer = self.get_buffer()
        buffer[2][7] = self.color_white
        buffer[2][8] = self.color_white
        buffer[2][9] = self.color_white
        buffer[3][6] = self.color_white
        buffer[3][7] = self.color_white
        buffer[3][9] = self.color_white
        buffer[3][10] = self.color_white
        buffer[4][5] = self.color_white
        buffer[4][6] = self.color_white
        buffer[4][10] = self.color_white
        buffer[4][11] = self.color_white
        buffer[5][5] = self.color_white
        buffer[5][11] = self.color_white
        buffer[6][5] = self.color_white
        buffer[6][6] = self.color_white
        buffer[7][6] = self.color_white
        buffer[7][7] = self.color_white
        buffer[8][7] = self.color_white
        buffer[8][8] = self.color_white
        buffer[8][9] = self.color_white
        buffer[7][9] = self.color_white
        buffer[7][10] = self.color_white
        buffer[6][10] = self.color_white
        buffer[6][11] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def test_draw_arc(self):
        self.lcd.draw_arc(5, 8, 3, 90, 270)
        buffer = self.get_buffer()
        buffer[2][7] = self.color_white
        buffer[2][8] = self.color_white
        buffer[2][9] = self.color_white
        buffer[3][6] = self.color_white
        buffer[3][7] = self.color_white
        buffer[3][9] = self.color_white
        buffer[3][10] = self.color_white
        buffer[4][5] = self.color_white
        buffer[4][6] = self.color_white
        buffer[4][10] = self.color_white
        buffer[4][11] = self.color_white
        buffer[5][5] = self.color_white
        buffer[5][11] = self.color_white
        assert_equal(self.drv.buffer, buffer)

    def draw_buffer(self, buffer):
        for y in range(self.lcd.height):
            row = ""
            for x in range(self.lcd.width):
                row += str(buffer[x][y])
            print (row)
