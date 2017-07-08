"""Null Area test chip driver"""
from gfxlcd.drawing.area import Area
from gfxlcd.abstract.chip import Chip


class NullArea(Area, Chip):
    """Test chip driver for area drawing"""
    def __init__(self, width, height, driver, auto_flush=True):
        Chip.__init__(self, width, height, driver, auto_flush)
        Area.__init__(self, driver)
        self.rotation = 0

    def _convert_color(self, color):
        """color color"""
        return color

    def init(self):
        """init display"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

    def _set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """set area to work on"""
        self.driver.area = {
            'start_x': pos_x1,
            'start_y': pos_y1,
            'end_x': pos_x2,
            'end_y': pos_y2
        }
        self.driver.pointer = (0, 0)
