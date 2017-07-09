"""ILI9325 chip driver"""
import time
from gfxlcd.drawing.area import Area
from gfxlcd.abstract.chip import Chip


class ILI9325(Area, Chip):
    """Class for ILI9325 based LCD"""
    rotations = {
        0: {
            'output': 0x0100,
            'mode': 0x1030,
            'output2': 0xa700
        },
        90: {
            'output': 0x0000,
            'mode': 0x1038,
            'output2': 0xa700
        },
        180: {
            'output': 0x0000,
            'mode': 0x1030,
            'output2': 0x2700
        },
        270: {
            'output': 0x0100,
            'mode': 0x1038,
            'output2': 0x2700
        }
    }

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

        # ************* ILI9325C/D **********
        # set SS and SM bit
        self.driver.cmd(0x0001, None)
        self.driver.data(self.rotations[self.rotation]['output'], None)

        # set 1 line inversion
        self.driver.cmd(0x0002, None)
        self.driver.data(0x0200, None)

        # set GRAM write direction and BGR=1
        self.driver.cmd(0x0003, None)
        self.driver.data(self.rotations[self.rotation]['mode'], None)

        # Resize register
        self.driver.cmd(0x0004, None)
        self.driver.data(0x0000, None)
        # set the back porch and front porch
        self.driver.cmd(0x0008, None)
        self.driver.data(0x0207, None)
        # set non-display area refresh cycle ISC[3:0]
        self.driver.cmd(0x0009, None)
        self.driver.data(0x0000, None)
        # FMARK function
        self.driver.cmd(0x000A, None)
        self.driver.data(0x0000, None)
        # RGB interface setting
        self.driver.cmd(0x000C, None)
        self.driver.data(0x0000, None)
        # Frame marker Position
        self.driver.cmd(0x000D, None)
        self.driver.data(0x0000, None)
        # RGB interface polarity
        self.driver.cmd(0x000F, None)
        self.driver.data(0x0000, None)

        # ************* Power On sequence ****************
        # SAP, BT[3:0], AP, DSTB, SLP, STB
        self.driver.cmd(0x0010, None)
        self.driver.data(0x0000, None)
        # DC1[2:0], DC0[2:0], VC[2:0]
        self.driver.cmd(0x0011, None)
        self.driver.data(0x0007, None)
        # VREG1OUT voltage
        self.driver.cmd(0x0012, None)
        self.driver.data(0x0000, None)
        # VDV[4:0] for VCOM amplitude
        self.driver.cmd(0x0013, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0007, None)
        self.driver.data(0x0001, None)
        time.sleep(0.2)  # Dis-charge capacitor power voltage
        # SAP, BT[3:0], AP, DSTB, SLP, STB
        self.driver.cmd(0x0010, None)
        self.driver.data(0x1690, None)
        # Set DC1[2:0], DC0[2:0], VC[2:0]
        self.driver.cmd(0x0011, None)
        self.driver.data(0x0227, None)
        time.sleep(0.05)
        self.driver.cmd(0x0012, None)
        self.driver.data(0x000D, None)
        time.sleep(0.05)
        # VDV[4:0] for VCOM amplitude
        self.driver.cmd(0x0013, None)
        self.driver.data(0x1200, None)
        # 04  VCM[5:0] for VCOMH
        self.driver.cmd(0x0029, None)
        self.driver.data(0x000A, None)
        # Set Frame Rate
        self.driver.cmd(0x002B, None)
        self.driver.data(0x000D, None)
        time.sleep(0.05)
        # GRAM horizontal Address
        self.driver.cmd(0x0020, None)
        self.driver.data(0x0000, None)
        # GRAM Vertical Address
        self.driver.cmd(0x0021, None)
        self.driver.data(0x0000, None)

        # ************* Adjust the Gamma Curve *************
        self.driver.cmd(0x0030, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0031, None)
        self.driver.data(0x0404, None)
        self.driver.cmd(0x0032, None)
        self.driver.data(0x0003, None)
        self.driver.cmd(0x0035, None)
        self.driver.data(0x0405, None)
        self.driver.cmd(0x0036, None)
        self.driver.data(0x0808, None)
        self.driver.cmd(0x0037, None)
        self.driver.data(0x0407, None)
        self.driver.cmd(0x0038, None)
        self.driver.data(0x0303, None)
        self.driver.cmd(0x0039, None)
        self.driver.data(0x0707, None)
        self.driver.cmd(0x003C, None)
        self.driver.data(0x0504, None)
        self.driver.cmd(0x003D, None)
        self.driver.data(0x0808, None)

        # ************* Set GRAM area *************
        # Horizontal GRAM Start Address
        self.driver.cmd(0x0050, None)
        self.driver.data(0x0000, None)
        # Horizontal GRAM End Address
        self.driver.cmd(0x0051, None)
        self.driver.data(0x00EF, None)
        # Vertical GRAM Start Address
        self.driver.cmd(0x0052, None)
        self.driver.data(0x0000, None)
        # Vertical GRAM Start Address
        self.driver.cmd(0x0053, None)
        self.driver.data(0x013F, None)
        # Gate Scan Line
        self.driver.cmd(0x0060, None)
        self.driver.data(self.rotations[self.rotation]['output2'], None)

        # NDL, VLE, REV
        self.driver.cmd(0x0061, None)
        self.driver.data(0x0001, None)
        # set scrolling line
        self.driver.cmd(0x006A, None)
        self.driver.data(0x0000, None)

        # ************* Partial Display Control *************
        self.driver.cmd(0x0080, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0081, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0082, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0083, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0084, None)
        self.driver.data(0x0000, None)
        self.driver.cmd(0x0085, None)
        self.driver.data(0x0000, None)

        # ************* Panel Control *************
        self.driver.cmd(0x0090, None)
        self.driver.data(0x0010, None)
        self.driver.cmd(0x0092, None)
        self.driver.data(0x0000, None)
        # 262K color and display ON
        self.driver.cmd(0x0007, None)
        self.driver.data(0x0133, None)

    def _set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """select area to work with"""
        if self.rotation == 90 or self.rotation == 270:
            pos_x1, pos_y1, pos_x2, pos_y2 = pos_y1, pos_x1, pos_y2, pos_x2
        self.driver.cmd(0x0020, None)
        self.driver.data(pos_x1, None)
        self.driver.cmd(0x0021, None)
        self.driver.data(pos_y1, None)
        self.driver.cmd(0x0050, None)
        self.driver.data(pos_x1, None)
        self.driver.cmd(0x0052, None)
        self.driver.data(pos_y1, None)
        self.driver.cmd(0x0051, None)
        self.driver.data(pos_x2, None)
        self.driver.cmd(0x0053, None)
        self.driver.data(pos_y2, None)
        self.driver.cmd(0x0022, None)
