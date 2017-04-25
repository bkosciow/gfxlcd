"""Area drawing algorithm"""
import itertools
from gfxlcd.drawing.pixel import Pixel


class Area(Pixel):
    """Area drawing algorithm"""
    def __init__(self, driver):
        self.driver = driver
        Pixel.__init__(self)

    def init(self):
        """additional initialization"""
        pass

    def draw_pixel(self, pos_x, pos_y):
        """draw one pixel"""
        self._set_area(pos_x, pos_y, pos_x, pos_y)
        self.driver.data(self._converted_color(), None)

    def _set_area(self, x1, y1, x2, y2):
        """select area to work with"""
        self.driver.cmd(0x0020, None)
        self.driver.data(x1, None)
        self.driver.cmd(0x0021, None)
        self.driver.data(y1, None)
        self.driver.cmd(0x0050, None)
        self.driver.data(x1, None)
        self.driver.cmd(0x0052, None)
        self.driver.data(y1, None)
        self.driver.cmd(0x0051, None)
        self.driver.data(x2, None)
        self.driver.cmd(0x0053, None)
        self.driver.data(y2, None)
        self.driver.cmd(0x0022, None)

    def _draw_vertical_line(self, pos_x, pos_y, length):
        """draw vertical line"""
        self._set_area(pos_x, pos_y, pos_x, pos_y + length)
        color = self._converted_color()
        for _ in itertools.repeat(None, length):
            self.driver.data(color, None)

    def _draw_horizontal_line(self, pos_x, pos_y, length):
        """draw horizontal line"""
        self._set_area(pos_x, pos_y, pos_x + length, pos_y)
        color = self._converted_color()
        for _ in itertools.repeat(None, length):
            self.driver.data(color, None)

    def _calculate_steps(self, length, step, required_length):
        """calculate lineparts - helper"""
        steps = [length for _ in range(0, step)]
        if step * length < required_length:
            for idx in range(0, required_length - step * length):
                steps[idx] += 1

        return steps

    def draw_line(self, x1, y1, x2, y2):
        """draw diagonal line"""
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        if x1 == x2:
            steps = [height]
            horizontal = False
            offset_x = offset_y = 0
        elif y1 == y2:
            steps = [width]
            horizontal = True
            offset_x = offset_y = 0
        elif width > height:
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            offset_y = 1 if y2 > y1 else -1
            offset_x = 1 if x2 > x1 else -1
            horizontal = True
            step = height
            length = width / step
            steps = self._calculate_steps(length, step, width)

        else:
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            offset_y = 1 if y2 > y1 else -1
            offset_x = 1 if x2 > x1 else -1
            horizontal = False
            step = width
            length = height / step
            steps = self._calculate_steps(length, step, height)

        delta_y = 0
        delta_x = 0
        for idx, step in enumerate(steps):
            if horizontal:
                self._draw_horizontal_line(
                    int(x1 + delta_x),
                    int(y1 + (idx * offset_y)),
                    int(step)
                )
                delta_x += step * offset_x
            else:
                self._draw_vertical_line(
                    int(x1 + (idx * offset_x)),
                    int(y1 + delta_y),
                    int(step)
                )
                delta_y += step * offset_y

    def fill_rect(self, x1, y1, x2, y2):
        """fill an area"""
        size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        self._set_area(
            min(x1, x2),
            min(y1, y2),
            max(x1, x2),
            max(y1, y2)
        )
        color = self._converted_background_color()
        for _ in range(0, size):
            self.driver.data(color, None)
