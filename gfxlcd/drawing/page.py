import abc
from gfxlcd.drawing.pixel import Pixel


class Page(Pixel, metaclass=abc.ABCMeta):
    """Page drawing algorithm"""
    def __init__(self, driver):
        self.driver = driver
        Pixel.__init__(self, driver)
        self.buffer = []

    def init(self):
        """init page"""
        if self.rotation == 0 or self.rotation == 180:
            self.buffer = [[0] * (self.height // 8) for x in range(self.width)]
        else:
            self.buffer = [[0] * (self.width // 8) for x in range(self.height)]

    def draw_pixel(self, pos_x, pos_y):
        """draw a pixel at x,y"""
        self.buffer[pos_x][pos_y//8] |= 1 << (pos_y % 8)
        self.flush()

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
                for appendix in range(int(step)):
                    self.draw_pixel(
                        int(pos_x1 + delta_x + appendix),
                        int(pos_y1 + (idx * offset_y))
                    )
                delta_x += step * offset_x
            else:
                for appendix in range(int(step)):
                    self.draw_pixel(
                        int(pos_x1 + (idx * offset_x)),
                        int(pos_y1 + delta_y + appendix)
                    )
                delta_y += step * offset_y

    def fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a filled rectangle"""
        if pos_y2 < pos_y1:
            pos_y1, pos_y2 = pos_y2, pos_y1
        if pos_x2 < pos_x1:
            pos_x1, pos_x2 = pos_x2, pos_x1
        start_page = pos_y1 // 8
        start_bit = pos_y1 % 8
        end_page = pos_y2 // 8
        end_bit = pos_y2 % 8
        rows = []
        first_page = int(('0' * start_bit).rjust(8, '1'), 2)
        last_page = int('1' * (end_bit+1), 2)
        if start_page != end_page:
            rows.append(first_page)
            for _ in range(end_page - start_page - 1):
                rows.append(255)
            rows.append(last_page)
        else:
            rows.append(first_page & last_page)

        page = start_page
        for value in rows:
            for x_diff in range(pos_x2-pos_x1+1):
                self.buffer[pos_x1+x_diff][page] |= value
            page += 1

    def get_page_value(self, column, page):
        """returns value"""
        return self.buffer[column][page]

    @abc.abstractmethod
    def flush(self, force=None):
        """flush buffer to the screen"""
        pass

    def draw_image(self, pos_x, pos_y, image):
        """draw a PIL image"""
        image_file = image.convert('L')
        width, height = image_file.size
        offset_x = 0
        offset_y = 0
        for stream in list(image_file.getdata()):
            if stream > self.options['threshold'] \
                    and not self._is_transparent(stream):
                self.draw_pixel(pos_x + offset_x, pos_y + offset_y)
            offset_x += 1
            if offset_x > width - 1:
                offset_x = 0
                offset_y += 1

    def _is_transparent(self, color):
        """check if color is a transparency color"""
        if type(self.options['transparency_color']) == int \
                and color == self.options['transparency_color']:
            return True
        elif type(self.options['transparency_color']) == list \
                and color in self.options['transparency_color']:
            return True

        return False
