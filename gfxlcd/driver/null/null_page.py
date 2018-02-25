"""Null Page test chip driver"""
from gfxlcd.drawing.page import Page
from gfxlcd.abstract.chip import Chip


class NullPage(Page, Chip):
    """Test chip driver for page drawing"""
    def __init__(self, width, height, driver, auto_flush=True):
        Chip.__init__(self, width, height, driver, auto_flush)
        Page.__init__(self, driver)
        self.rotation = 0
        self.buffer = []
        self.area = {
            'start_x': 0,
            'start_y': 0,
            'end_x': width-1,
            'end_y': height-1
        }

    def init(self):
        """inits a device"""
        Page.init(self)
        Chip.init(self)

    def flush(self, force=None):
        """flush buffer to device
        :force - boolean|None"""
        return self.buffer

    def set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """set area to work on"""
        self.area = {
            'start_x': pos_x1,
            'start_y': pos_y1,
            'end_x': pos_x2,
            'end_y': pos_y2
        }
