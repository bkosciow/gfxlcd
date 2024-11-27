from gfxlcd.drawing.area import Area
from gfxlcd.abstract.chip import Chip
import time


class ST7789(Area, Chip):
    rotations = {0: 0x88, 90: 0xf8, 180: 0x48, 270: 0x28}
    def __init__(self, width, height, driver):
        Chip.__init__(self, width, height, driver, True)
        Area.__init__(self, driver)

    def _convert_color(self, color):
        """color from 8-8-8 to 5-6-5"""
        return (color['R'] & 0xF8) << 8 | (color['G'] & 0xFC) << 3 | color['B'] >> 3
        rgb = color['R'] << 16 | \
            color['G'] << 8 | \
            color['B']
        return ((rgb & 0x00f80000) >> 8) |\
            ((rgb & 0x0000fc00) >> 5) | ((rgb & 0x000000f8) >> 3)

    def init(self):
        """Initialize dispaly"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

        self.command(0x36)
        self.data(0x70)  # self.data(0x00)

        self.command(0x3A)
        self.data(0x05)

        self.command(0xB2)
        self.data(0x0C)
        self.data(0x0C)
        self.data(0x00)
        self.data(0x33)
        self.data(0x33)

        self.command(0xB7)
        self.data(0x35)

        self.command(0xBB)
        self.data(0x19)
        self.command(0xC0)

        self.data(0x2C)

        self.command(0xC2)
        self.data(0x01)

        self.command(0xC3)
        self.data(0x12)

        self.command(0xC4)
        self.data(0x20)

        self.command(0xC6)
        self.data(0x0F)



        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)


        self.command(0xE0)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0D)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2B)
        self.data(0x3F)
        self.data(0x54)
        self.data(0x4C)
        self.data(0x18)
        self.data(0x0D)
        self.data(0x0B)
        self.data(0x1F)
        self.data(0x23)

        self.command(0xE1)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0C)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2C)
        self.data(0x3F)
        self.data(0x44)
        self.data(0x51)
        self.data(0x2F)
        self.data(0x1F)
        self.data(0x1F)
        self.data(0x20)
        self.data(0x23)

        self.command(0x21)

        self.command(0x11)

        self.command(0x29)

    def data(self, d):
        self.driver.data(d, None)

    def command(self, c):
        self.driver.cmd(c, None)

    def init2(self):
        """init display"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

        self.driver.cmd(0x11, None)
        self.driver.data(0x00, None)
        time.sleep(0.200)

        self.driver.cmd(0x13, None)
        self.driver.data(0x00, None)

        self.driver.cmd(0xb6, None)
        self.driver.data(0x0a, None)
        self.driver.data(0x82, None)

        self.driver.cmd(0x3a, None)
        self.driver.data(0x55, None)

        self.driver.cmd(0xB2, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x00, None)
        self.driver.data(0x33, None)
        self.driver.data(0x33, None)

        self.driver.cmd(0xB7, None)
        self.driver.data(0x35, None)

        self.driver.cmd(0xBB, None)
        self.driver.data(0x28, None)

        self.driver.cmd(0xC0, None)
        self.driver.data(0x0C, None)

        self.driver.cmd(0xC2, None)
        self.driver.data(0x01, None)
        self.driver.data(0xFF, None)

        self.driver.cmd(0xC3, None)
        self.driver.data(0x10, None)

        self.driver.cmd(0xC4, None)
        self.driver.data(0x20, None)

        self.driver.cmd(0xC6, None)
        self.driver.data(0x0F, None)

        self.driver.cmd(0xD0, None)
        self.driver.data(0xA4, None)
        self.driver.data(0xA1, None)

        self.driver.cmd(0xE0, None)  # Set Gamma
        self.driver.data(0xD0, None)
        self.driver.data(0x00, None)
        self.driver.data(0x02, None)
        self.driver.data(0x07, None)
        self.driver.data(0x0a, None)
        self.driver.data(0x28, None)
        self.driver.data(0x32, None)
        self.driver.data(0x44, None)
        self.driver.data(0x42, None)
        self.driver.data(0x06, None)
        self.driver.data(0x0e, None)
        self.driver.data(0x12, None)
        self.driver.data(0x14, None)
        self.driver.data(0x27, None)

        self.driver.cmd(0xE1, None)  # Set Gamma
        self.driver.data(0xD0, None)
        self.driver.data(0x04, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x11, None)
        self.driver.data(0x13, None)
        self.driver.data(0x2C, None)
        self.driver.data(0x3F, None)
        self.driver.data(0x44, None)
        self.driver.data(0x51, None)
        self.driver.data(0x2F, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x20, None)
        self.driver.data(0x23, None)

        self.driver.cmd(0x20, None)
        self.driver.data(0x00, None)

        self.driver.cmd(0x29, None)
        self.driver.data(0x00, None)

        time.sleep(0.100)

    def init_2(self):
        """init display"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

        self.driver.cmd(0x01, None)
        time.sleep(0.200)

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

    def init_(self):
        """init display"""
        self.driver.init()
        Area.init(self)
        Chip.init(self)
        self.driver.reset()

        # reset
        self.driver.cmd(0x01, None)
        time.sleep(0.200)

        # self.driver.cmd(0x36, None)
        # self.driver.data(0x70, None)
        # self.driver.cmd(0x3A, None)
        # self.driver.data(0x05, None)

        self.driver.cmd(0x36, None)
        self.driver.data(0x70, None)
        #
        self.driver.cmd(0xB2, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x00, None)
        self.driver.data(0x33, None)
        self.driver.data(0x33, None)
        #
        self.driver.cmd(0x3A, None)
        self.driver.data(0x05, None)
        #
        self.driver.cmd(0xB7, None)
        self.driver.data(0x14, None)
        #
        self.driver.cmd(0xBB, None)
        self.driver.data(0x37, None)

        self.driver.cmd(0xC0, None)
        self.driver.data(0x2C, None)

        self.driver.cmd(0xC2, None)
        self.driver.data(0x01, None)

        self.driver.cmd(0xC3, None)
        self.driver.data(0x12, None)

        self.driver.cmd(0xC4, None)
        self.driver.data(0x20, None)

        self.driver.cmd(0xD0, None)
        self.driver.data(0xA4, None)
        self.driver.data(0xA1, None)

        self.driver.cmd(0xC6, None)
        self.driver.data(0x0F, None)

        self.driver.cmd(0xE0, None)  # Set Gamma
        self.driver.data(0xD0, None)
        self.driver.data(0x04, None)
        self.driver.data(0x0D, None)
        self.driver.data(0x11, None)
        self.driver.data(0x13, None)
        self.driver.data(0x2B, None)
        self.driver.data(0x3F, None)
        self.driver.data(0x54, None)
        self.driver.data(0x4C, None)
        self.driver.data(0x18, None)
        self.driver.data(0x0D, None)
        self.driver.data(0x0B, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x23, None)

        self.driver.cmd(0xE1, None)  # Set Gamma
        self.driver.data(0xD0, None)
        self.driver.data(0x04, None)
        self.driver.data(0x0C, None)
        self.driver.data(0x11, None)
        self.driver.data(0x13, None)
        self.driver.data(0x2C, None)
        self.driver.data(0x3F, None)
        self.driver.data(0x44, None)
        self.driver.data(0x51, None)
        self.driver.data(0x2F, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x1F, None)
        self.driver.data(0x20, None)
        self.driver.data(0x23, None)

        self.driver.cmd(0x20, None)
        self.driver.cmd(0x11, None)
        self.driver.cmd(0x29, None)

        time.sleep(0.100)

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

    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self._set_area ( 0, 0, self.width, self.height)
        for i in range(0,len(_buffer),4096):
            self.driver.data(0xff, None)