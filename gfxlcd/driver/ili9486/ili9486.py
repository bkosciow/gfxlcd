"""ILI9486 chip driver"""
from gfxlcd.drawing.area import Area
from gfxlcd.abstract.chip import Chip


class ILI9486(Area, Chip):
    """Class for ILI9486 based LCD"""
    rotations = {0: 0x88, 90: 0xf8, 180: 0x48, 270: 0x28}

    def __init__(self, width, height, driver):
        Chip.__init__(self, width, height, driver, True)
        Area.__init__(self, driver)

    def _convert_color(self, color):
        """color from 8-8-8 to 5-6-5"""
        rgb = color['R'] << 16 | \
            color['G'] << 8 | \
            color['B']
        return ((rgb & 0x00f80000) >> 8) |\
            ((rgb & 0x0000fc00) >> 5) | ((rgb & 0x000000f8) >> 3)

    def init(self):
        """init display"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

        # Read Display MADCTL
        self.driver.cmd(0x0b, None)
        self.driver.data(0x00, None)
        self.driver.data(0x00, None)

        # Sleep OUT
        self.driver.cmd(0x11, None)

        # Interface Pixel Format
        self.driver.cmd(0x3a, None)
        self.driver.data(0x55, None) #0x66 5-6-5 / 55 6-6-6

        # Memory Access Control (
        self.driver.cmd(0x36, None)
        self.driver.data(self.rotations[self.rotation], None)

        # Power Control 3 (For Normal Mode)
        self.driver.cmd(0xc2, None)
        self.driver.data(0x44, None)

        # VCOM Control
        self.driver.cmd(0xc5, None)
        self.driver.data(0x00, None)
        self.driver.data(0x00, None)
        self.driver.data(0x00, None)
        self.driver.data(0x00, None)

        # PGAMCTRL(Positive Gamma Control)
        self.driver.cmd(0xe0, None)
        self.driver.data(0x0F, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x1C, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x0F, None)
        self.driver.data(0x08, None)
        self.driver.data(0x48, None)
        self.driver.data(0x98, None)
        self.driver.data(0x37, None)
        self.driver.data(0x0A, None)
        self.driver.data(0x13, None)
        self.driver.data(0x04, None)
        self.driver.data(0x11, None)
        self.driver.data(0x0D, None)
        self.driver.data(0x00, None)

        # NGAMCTRL (Negative Gamma Correction)
        self.driver.cmd(0xe1, None)
        self.driver.data(0x0F, None)
        self.driver.data(0x32, None)
        self.driver.data(0x2E, None)
        self.driver.data(0x0B, None)
        self.driver.data(0x0D, None)
        self.driver.data(0x05, None)
        self.driver.data(0x47, None)
        self.driver.data(0x75, None)
        self.driver.data(0x37, None)
        self.driver.data(0x06, None)
        self.driver.data(0x10, None)
        self.driver.data(0x03, None)
        self.driver.data(0x24, None)
        self.driver.data(0x20, None)
        self.driver.data(0x00, None)

        # Digital Gamma Control 1
        self.driver.cmd(0xe2, None)
        self.driver.data(0x0F, None)
        self.driver.data(0x32, None)
        self.driver.data(0x2E, None)
        self.driver.data(0x0B, None)
        self.driver.data(0x0D, None)
        self.driver.data(0x05, None)
        self.driver.data(0x47, None)
        self.driver.data(0x75, None)
        self.driver.data(0x37, None)
        self.driver.data(0x06, None)
        self.driver.data(0x10, None)
        self.driver.data(0x03, None)
        self.driver.data(0x24, None)
        self.driver.data(0x20, None)
        self.driver.data(0x00, None)

        # Sleep OUT
        self.driver.cmd(0x11, None)

        # Display ON
        self.driver.cmd(0x29, None)

    def _set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """select area to work with"""
        self.driver.cmd(0x2a, None)
        self.driver.data(pos_x1 >> 8, None)
        self.driver.data(pos_x1 & 0xff, None)
        self.driver.data(pos_x2 >> 8, None)
        self.driver.data(pos_x2 & 0xff, None)
        self.driver.cmd(0x2b, None)
        self.driver.data(pos_y1 >> 8, None)
        self.driver.data(pos_y1 & 0xff, None)
        self.driver.data(pos_y2 >> 8, None)
        self.driver.data(pos_y2 & 0xff, None)
        self.driver.cmd(0x2c, None)
