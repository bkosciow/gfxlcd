"""SSD1306 chip driver"""
from gfxlcd.drawing.page import Page
from gfxlcd.abstract.chip import Chip


class SSD1306(Page, Chip):
    """Class for an LCD with SSD306 chip"""
    rotations = {
        0: {
            'sgmt': 0xa1,
            'com': 0xc8
        },
        90: {
            'sgmt': 0xa0,
            'com': 0xc8
        },
        180: {
            'sgmt': 0xa0,
            'com': 0xc0
        },
        270: {
            'sgmt': 0xa1,
            'com': 0xc0
        }
    }

    def __init__(self, width, height, driver, auto_flush=False):
        Chip.__init__(self, width, height, driver, auto_flush)
        Page.__init__(self, driver)
        self.rotation = 0
        self.offset_j = 1
        self.xy_callback = None

    def init(self):
        """inits a device"""
        self.driver.init()
        Page.init(self)
        Chip.init(self)
        self.driver.reset()
        self.driver.cmd(0xae)  # turn off panel
        self.driver.cmd(0x00)  # set low column address
        self.driver.cmd(0x10)  # set high column address
        self.driver.cmd(0x40)  # set start line address

        self.driver.cmd(0x20)  # addr mode
        self.driver.cmd(0x02)  # horizontal

        self.driver.cmd(0xb0)  # set page address
        self.driver.cmd(0x81)  # set contrast control register
        self.driver.cmd(0xff)
        # a0/a1, a1 = segment 127 to 0, a0:0 to seg127
        self.driver.cmd(self.rotations[self.rotation]['sgmt'])

        # c8/c0 set com(N-1)to com0  c0:com0 to com(N-1)
        self.driver.cmd(self.rotations[self.rotation]['com'])

        self.driver.cmd(0xa6)  # set normal display, a6 - normal, a7 - inverted

        self.driver.cmd(0xa8)  # set multiplex ratio(16to63)
        self.driver.cmd(0x3f)  # 1/64 duty

        self.driver.cmd(0xd3)  # set display offset
        self.driver.cmd(0x00)  # not offset

        # set display clock divide ratio/oscillator frequency
        self.driver.cmd(0xd5)
        self.driver.cmd(0x80)  # set divide ratio

        self.driver.cmd(0xd9)  # set pre-charge period
        self.driver.cmd(0xf1)
        self.driver.cmd(0xda)  # set com pins hardware configuration
        self.driver.cmd(0x12)

        self.driver.cmd(0xdb)  # set vcomh
        self.driver.cmd(0x40)

        self.driver.cmd(0x8d)  # charge pump
        self.driver.cmd(0x14)  # enable charge pump
        self.driver.cmd(0xaf)  # turn on panel

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
                self.set_area(0, j, width-1, j+self.offset_j)
                for i in range(0, width):
                    if self.xy_callback is not None:
                        (i, j) = self.xy_callback(self, i, j)
                    self.driver.data(self.get_page_value(i, j))

    def set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """set area to work on"""
        self.driver.cmd(0x22)
        self.driver.cmd(0xb0 + pos_y1)
        self.driver.cmd(0xb0 + pos_y2)
        self.driver.cmd(0x21)
        self.driver.cmd(pos_x1)
        self.driver.cmd(pos_x2)

    def draw_pixel(self, pos_x, pos_y, color=None):
        """draw a pixel at x,y"""
        if self.rotation == 90 or self.rotation == 270:
            pos_x, pos_y = pos_y, pos_x
        Page.draw_pixel(self, pos_x, pos_y, color)
