"""Area drawing algorithm"""
import itertools
from gfxlcd.drawing.pixel import Pixel
from PIL import Image


class Area(Pixel):
    """Area drawing algorithm"""
    def __init__(self, driver):
        self.driver = driver
        Pixel.__init__(self, driver)

    def init(self):
        """additional initialization"""
        pass

    def draw_pixel(self, pos_x, pos_y, color=None):
        """draw one pixel"""
        if color is None:
            color = self.options['color']
        self._set_area(pos_x, pos_y, pos_x, pos_y)
        self.driver.data(self._convert_color(color), None)

    def _draw_vertical_line(self, pos_x, pos_y, length):
        """draw vertical line"""
        self._set_area(pos_x, pos_y, pos_x, pos_y + length)
        color = self._convert_color(self.options['color'])
        for _ in itertools.repeat(None, length):
            self.driver.data(color, None)

    def _draw_horizontal_line(self, pos_x, pos_y, length):
        """draw horizontal line"""
        self._set_area(pos_x, pos_y, pos_x + length, pos_y)
        color = self._convert_color(self.options['color'])
        for _ in itertools.repeat(None, length):
            self.driver.data(color, None)

    def draw_line(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw diagonal line"""
        width = abs(pos_x2 - pos_x1)
        height = abs(pos_y2 - pos_y1)
        if pos_x1 == pos_x2:
            steps = [height+1]
            horizontal = False
            offset_x = offset_y = 0
        elif pos_y1 == pos_y2:
            steps = [width+1]
            horizontal = True
            offset_x = offset_y = 0
        elif width > height:
            width += 1
            if pos_x2 < pos_x1:
                pos_x1, pos_x2 = pos_x2, pos_x1
                pos_y1, pos_y2 = pos_y2, pos_y1
            offset_y = 1 if pos_y2 > pos_y1 else -1
            offset_x = 1 if pos_x2 > pos_x1 else -1
            horizontal = True
            step = height + 1
            length = width // step
            steps = self._calculate_line_steps(length, step, width)
        else:
            height += 1
            if pos_y2 < pos_y1:
                pos_x1, pos_x2 = pos_x2, pos_x1
                pos_y1, pos_y2 = pos_y2, pos_y1
            offset_y = 1 if pos_y2 > pos_y1 else -1
            offset_x = 1 if pos_x2 > pos_x1 else -1
            horizontal = False
            step = width + 1
            length = height // step
            steps = self._calculate_line_steps(length, step, height)

        delta_y = 0
        delta_x = 0
        for idx, step in enumerate(steps):
            if horizontal:
                self._draw_horizontal_line(
                    int(pos_x1 + delta_x),
                    int(pos_y1 + (idx * offset_y)),
                    int(step)
                )
                delta_x += step * offset_x
            else:
                self._draw_vertical_line(
                    int(pos_x1 + (idx * offset_x)),
                    int(pos_y1 + delta_y),
                    int(step)
                )
                delta_y += step * offset_y

    def fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """fill an area"""
        size = (abs(pos_x2 - pos_x1) + 1) * (abs(pos_y2 - pos_y1) + 1)
        self._set_area(
            min(pos_x1, pos_x2),
            min(pos_y1, pos_y2),
            max(pos_x1, pos_x2),
            max(pos_y1, pos_y2)
        )
        # color = self._converted_background_color()
        color = self._convert_color(self.options['background_color'])
        for _ in range(0, size):
            self.driver.data(color, None)

    def draw_image(self, pos_x, pos_y, image):
        """draw a PIL image"""
        if isinstance(image, str):
            image = Image.open(image)
        image_file = image.convert('RGB')
        width, height = image_file.size
        self._set_area(
            pos_x,
            pos_y,
            pos_x + width - 1,
            pos_y + height - 1
        )
        row = 0
        col = 0
        area = None
        temporary_area = None
        for red, green, blue in list(image_file.getdata()):
            if self._is_transparent((red, green, blue)):
                area = (
                    pos_x,
                    pos_y + row + 1,
                    pos_x + width - 1,
                    pos_y + height - 1
                )
                temporary_area = (
                    pos_x + col + 1,
                    pos_y + row,
                    pos_x + width - 1,
                    pos_y + row
                )
            else:
                if temporary_area is not None:
                    self._set_area(*temporary_area)
                    temporary_area = None
                self.color = (red, green, blue)
                self.driver.data(
                    self._convert_color(self.options['color']), None
                )

            col += 1
            if col > width - 1:
                col = 0
                row += 1
                if area is not None:
                    self._set_area(*area)
                    area = None
                    temporary_area = None

    def _is_transparent(self, color):
        """check if color is a transparency color"""
        if self.options['transparency_color'] is None:
            return False
        elif type(self.options['transparency_color'][0]) == int \
            and color == self.options['transparency_color']:
                return True
        elif (type(self.options['transparency_color'][0]) == list or
            type(self.options['transparency_color'][0]) == tuple) \
            and color in self.options['transparency_color']:
                return True

        return False

    def _draw_letter(self, pos_x, pos_y, letter, with_background=False):
        """draw a letter"""
        if not with_background:
            super()._draw_letter(pos_x, pos_y, letter, with_background)
        else:
            font = self.options['font']
            self._set_area(
                pos_x,
                pos_y,
                pos_x + font.size[0] - 1,
                pos_y + font.size[1] - 1
            )

            bits = font.size[0]
            color = self._convert_color(self.options['color'])
            background_color = self._convert_color(self.options['background_color'])
            for row, data in enumerate(font.get(letter)):
                for bit in range(bits):
                    if data & 0x01:
                        self.driver.data(color, None)
                    else:
                        self.driver.data(background_color, None)
                    data >>= 1
