"""NJU6450 chip"""
from gfxlcd.drawing.page import Page
from gfxlcd.abstract.chip import Chip


class NJU6450(Page, Chip):
    """Class for an LCD with NJU6450 chip"""
    def __init__(self, width, height, driver, auto_flush=True):
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
        if pos_x < self.width/2:
            self.driver.cmd(0xB8 | pos_y, 0)
            self.driver.cmd(0x00 | pos_x, 0)
        else:
            self.driver.cmd(0xB8 | pos_y, 1)
            self.driver.cmd(0x00 | (pos_x - self.width//2), 1)

    def _converted_background_color(self):
        """convert RGB background to available color"""
        return 1

    def _converted_color(self):
        """convert RGB color to available color"""
        return 1

    def flush(self, force=None):
        """flush buffer to device
        :force - boolean|None"""
        if force is None:
            force = self.options['auto_flush']

        if force:
            for j in range(0, self.height//8):
                for i in range(0, self.width):
                    self.set_xy(i, j)
                    if i < self.width/2:
                        self.driver.data(self.get_page_value(i, j), 0)
                    else:
                        self.driver.data(self.get_page_value(i, j), 1)
