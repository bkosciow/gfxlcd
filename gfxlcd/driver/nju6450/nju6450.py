"""NJU6450 chip"""
from gfxlcd.drawing.page import Page
from gfxlcd.abstract.chip import Chip


class NJU6450(Page, Chip):
    """Class for an LCD with NJU6450 chip"""
    def __init__(self, width, height, driver, auto_flush=False):
        Chip.__init__(self, width, height, driver, auto_flush)
        Page.__init__(self, driver)
        self.rotation = 0

    def init(self):
        """initialize display"""
        self.driver.init()
        Page.init(self)
        Chip.init(self)
        self.driver.reset()

        init_sequence = [0xae, 0xa4, 0xa9, 0xe2, 0xa0, 0xaf]
        for cmd in init_sequence:
            self.driver.cmd(cmd, 0)
            self.driver.cmd(cmd, 1)

    def set_xy(self, pos_x, pos_y):
        """set xy pos"""
        if self.rotation == 0 or self.rotation == 180:
            width = self.width
        else:
            width = self.height
        if pos_x < width//2:
            self.driver.cmd(0xB8 | pos_y, 0)
            self.driver.cmd(0x00 | pos_x, 0)
        else:
            self.driver.cmd(0xB8 | pos_y, 1)
            self.driver.cmd(0x00 | (pos_x - width//2), 1)

    def flush(self, force=None):
        """flush buffer to device
        :force - boolean|None"""
        if force is None:
            force = self.options['auto_flush']

        if force:
            if self.rotation == 0 or self.rotation == 180:
                height, width = self.height, self.width
            else:
                width, height = self.height, self.width
            for j in range(0, height//8):
                for i in range(0, width):
                    self.set_xy(i, j)
                    if i < width//2:
                        self.driver.data(self.get_page_value(i, j), 0)
                    else:
                        self.driver.data(self.get_page_value(i, j), 1)

    def draw_pixel(self, pos_x, pos_y, color=None):
        """draw a pixel at x,y"""
        if self.rotation == 90:
            pos_x, pos_y = self.height - pos_y - 1, pos_x
        if self.rotation == 180:
            pos_x, pos_y = self.width - pos_x - 1, self.height - pos_y - 1
        if self.rotation == 270:
            pos_x, pos_y = pos_y, self.width - pos_x - 1
        Page.draw_pixel(self, pos_x, pos_y, color)

    def fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a filled rectangle"""
        if self.rotation == 90:
            pos_x1, pos_y1 = self.height - pos_y1 - 1, pos_x1
            pos_x2, pos_y2 = self.height - pos_y2 - 1, pos_x2
        if self.rotation == 180:
            pos_x1, pos_y1 = self.width - pos_x1 - 1, self.height - pos_y1 - 1
            pos_x2, pos_y2 = self.width - pos_x2 - 1, self.height - pos_y2 - 1
        if self.rotation == 270:
            pos_x1, pos_y1 = pos_y1, self.width - pos_x1 - 1
            pos_x2, pos_y2 = pos_y2, self.width - pos_x2 - 1
        Page.fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2)
