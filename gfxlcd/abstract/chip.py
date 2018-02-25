"""Chip interface"""
import abc
from gfxlcd.font.font8x8 import Font8x8


class Chip(metaclass=abc.ABCMeta):
    """Chip class"""
    def __init__(self, width, height, driver, auto_flush):
        self.options = {}
        self.rotation = 0
        self._width = width
        self._height = height
        self.driver = driver
        self.options['auto_flush'] = auto_flush
        self.options['font'] = Font8x8()

    @property
    def width(self):
        """get width"""
        if self.rotation == 0 or self.rotation == 180:
            return self._width
        return self._height

    @property
    def height(self):
        """get height"""
        if self.rotation == 0 or self.rotation == 180:
            return self._height
        return self._width

    @abc.abstractmethod
    def _convert_color(self, color):
        """convert color to avaible one"""
        pass

    @property
    def color(self):
        """get RGB colour"""
        return self.options['color']

    @color.setter
    def color(self, rgb):
        """set (R, G, B) colour """
        if isinstance(rgb, int):
            self.options['color'] = rgb
        else:
            self.options['color'] = {
                'R': rgb[0], 'G': rgb[1], 'B': rgb[2]
            }

    @property
    def background_color(self):
        """get background colour"""
        return self.options['background_color']

    @background_color.setter
    def background_color(self, rgb):
        """set (R, G, B) background colour """
        if isinstance(rgb, int):
            self.options['background_color'] = rgb
        else:
            self.options['background_color'] = {
                'R': rgb[0], 'G': rgb[1], 'B': rgb[2]
            }

    @property
    def auto_flush(self):
        """get auto_flush"""
        return self.options['auto_flush']

    @auto_flush.setter
    def auto_flush(self, value):
        """set auto_flush"""
        self.options['auto_flush'] = bool(value)

    @property
    def font(self):
        """get current font"""
        return self.options['font']

    @font.setter
    def font(self, font):
        """set ttf font"""
        self.options['font'] = font

    @abc.abstractmethod
    def init(self):
        """init a chipset"""
        pass

    @abc.abstractmethod
    def draw_pixel(self, pos_x, pos_y, color=None):
        """draw a pixel at x,y"""
        pass

    @abc.abstractmethod
    def draw_line(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a line from point x1,y1 to x2,y2"""
        pass

    @abc.abstractmethod
    def draw_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a rectangle"""
        pass

    @abc.abstractmethod
    def draw_circle(self, pos_x, pos_y, radius):
        """draw a circle"""
        pass

    @abc.abstractmethod
    def draw_arc(self, pos_x, pos_y, radius, start, end):
        """draw an arc"""
        pass

    @abc.abstractmethod
    def fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a filled rectangle"""
        pass

    @abc.abstractmethod
    def draw_image(self, pos_x, pos_y, image):
        """draw a PIL image"""
        pass

    @abc.abstractmethod
    def draw_text(self, pos_x, pos_y, text):
        """draw a text"""
        pass
