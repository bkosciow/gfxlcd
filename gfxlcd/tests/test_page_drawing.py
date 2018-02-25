import sys
from nose.tools import assert_equal
sys.path.append("../../")
from gfxlcd.driver.null.null_page import NullPage


class TestPageDrawing(object):
    def setUp(self):
        self.lcd = NullPage(10, 16, None, False)
        self.lcd.init()

    def get_buffer(self):
        return [[0] * (16 // 8) for x in range(10)]

    def test_has_correct_size(self):
        assert_equal(self.lcd.width, 10)
        assert_equal(self.lcd.height, 16)

    def test_empty_buffer_after_init(self):
        assert_equal(self.lcd.buffer, self.get_buffer())

    def test_draw_pixel(self):
        self.lcd.draw_pixel(1, 1)
        buffer = self.get_buffer()
        buffer[1][0] = 2
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_pixels_on_same_page(self):
        self.lcd.draw_pixel(1, 1)
        self.lcd.draw_pixel(1, 4)
        buffer = self.get_buffer()
        buffer[1][0] = 18
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_pixels_on_different_pages(self):
        self.lcd.draw_pixel(2, 9)
        self.lcd.draw_pixel(1, 4)
        buffer = self.get_buffer()
        buffer[1][0] = 16
        buffer[2][1] = 2
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_horizontal_line(self):
        self.lcd.draw_line(1, 1, 8, 1)
        buffer = self.get_buffer()
        buffer[1][0] = 2
        buffer[2][0] = 2
        buffer[3][0] = 2
        buffer[4][0] = 2
        buffer[5][0] = 2
        buffer[6][0] = 2
        buffer[7][0] = 2
        buffer[8][0] = 2
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_vertical_line(self):
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][0] = 254
        buffer[1][1] = 127
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_overlapping_lines(self):
        self.lcd.draw_line(1, 1, 8, 1)
        self.lcd.draw_line(1, 1, 1, 14)
        buffer = self.get_buffer()
        buffer[1][0] = 254
        buffer[2][0] = 2
        buffer[3][0] = 2
        buffer[4][0] = 2
        buffer[5][0] = 2
        buffer[6][0] = 2
        buffer[7][0] = 2
        buffer[8][0] = 2
        buffer[1][1] = 127
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_diagonal_line(self):
        self.lcd.draw_line(0, 0, 9, 1)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 1
        buffer[2][0] = 1
        buffer[3][0] = 1
        buffer[4][0] = 1
        buffer[5][0] = 2
        buffer[6][0] = 2
        buffer[7][0] = 2
        buffer[8][0] = 2
        buffer[9][0] = 2
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_diagonal_line_even_steps(self):
        self.lcd.draw_line(0, 0, 9, 15)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 2
        buffer[2][0] = 4+8
        buffer[3][0] = 16+32
        buffer[4][0] = 128+64
        buffer[5][1] = 1+2
        buffer[6][1] = 4+8
        buffer[7][1] = 16+32
        buffer[8][1] = 64
        buffer[9][1] = 128
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_diagonal_line_even_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 5)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 2
        buffer[2][0] = 2
        buffer[3][0] = 4
        buffer[4][0] = 4
        buffer[5][0] = 8
        buffer[6][0] = 8
        buffer[7][0] = 16
        buffer[8][0] = 16
        buffer[9][0] = 32
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_diagonal_line_odd_steps_even_rest(self):
        self.lcd.draw_line(0, 0, 9, 6)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 2
        buffer[2][0] = 4
        buffer[3][0] = 4
        buffer[4][0] = 8
        buffer[5][0] = 8
        buffer[6][0] = 16
        buffer[7][0] = 16
        buffer[8][0] = 32
        buffer[9][0] = 64
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_diagonal_line_even_steps_odd_rest(self):
        self.lcd.draw_line(0, 0, 8, 6)
        buffer = self.get_buffer()
        buffer[0][0] = 1
        buffer[1][0] = 2
        buffer[2][0] = 4
        buffer[3][0] = 8
        buffer[4][0] = 8
        buffer[5][0] = 8
        buffer[6][0] = 16
        buffer[7][0] = 32
        buffer[8][0] = 64
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_rect(self):
        self.lcd.draw_rect(2, 2, 7, 11)
        buffer = self.get_buffer()
        buffer[2][0] = 4+8+16+32+64+128
        buffer[3][0] = 4
        buffer[4][0] = 4
        buffer[5][0] = 4
        buffer[6][0] = 4
        buffer[7][0] = 4+8+16+32+64+128

        buffer[2][1] = 1+2+4+8
        buffer[3][1] = 8
        buffer[4][1] = 8
        buffer[5][1] = 8
        buffer[6][1] = 8
        buffer[7][1] = 1+2+4+8
        assert_equal(self.lcd.buffer, buffer)

    def test_fill_rect(self):
        self.lcd.fill_rect(2, 2, 7, 11)
        buffer = self.get_buffer()
        buffer[2][0] = 4+8+16+32+64+128
        buffer[3][0] = 4+8+16+32+64+128
        buffer[4][0] = 4+8+16+32+64+128
        buffer[5][0] = 4+8+16+32+64+128
        buffer[6][0] = 4+8+16+32+64+128
        buffer[7][0] = 4+8+16+32+64+128
        buffer[2][1] = 1+2+4+8
        buffer[3][1] = 1+2+4+8
        buffer[4][1] = 1+2+4+8
        buffer[5][1] = 1+2+4+8
        buffer[6][1] = 1+2+4+8
        buffer[7][1] = 1+2+4+8
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_circle(self):
        self.lcd.draw_circle(5, 8, 3)
        buffer = self.get_buffer()
        buffer[2][0] = 128
        buffer[3][0] = 64+128
        buffer[4][0] = 32+64
        buffer[5][0] = 32
        buffer[6][0] = 32+64
        buffer[7][0] = 64+128
        buffer[8][0] = 128
        buffer[2][1] = 1+2
        buffer[3][1] = 2+4
        buffer[4][1] = 4+8
        buffer[5][1] = 8
        buffer[6][1] = 4+8
        buffer[7][1] = 2+4
        buffer[8][1] = 1+2
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_arc(self):
        self.lcd.draw_arc(5, 8, 3, 90, 270)
        buffer = self.get_buffer()
        buffer[2][0] = 128
        buffer[3][0] = 64+128
        buffer[4][0] = 32+64
        buffer[5][0] = 32
        buffer[2][1] = 1+2
        buffer[3][1] = 2+4
        buffer[4][1] = 4+8
        buffer[5][1] = 8
        assert_equal(self.lcd.buffer, buffer)

    def test_draw_pixels_clear_then(self):
        self.lcd.draw_pixel(1, 1)
        self.lcd.draw_pixel(2, 1)
        self.lcd.draw_pixel(2, 2)
        buffer = self.get_buffer()
        buffer[2][0] = 4
        self.lcd.draw_pixel(1, 1, self.lcd.background_color)
        self.lcd.draw_pixel(2, 1, self.lcd.background_color)
        self.draw_buffer(self.lcd.buffer)
        assert_equal(self.lcd.buffer, buffer)

    def draw_buffer(self, buffer):
        for page in range(2):
            print(page)
            row = ""
            for y in [1, 2, 4, 8, 16, 32, 64, 128]:
                for x in range(10):
                    if buffer[x][page] & y:
                        row += "#"
                    else:
                        row += "_"
                print(row)
                row = ""
