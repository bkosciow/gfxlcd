"""Driver for CharLCD module
allows graphical LCD to work as character LCD
"""
from charlcd.drivers.base import BaseDriver
from charlcd.abstract.flush_event_interface import FlushEvent


class HD44780(BaseDriver, FlushEvent):
    """HD44780 driver for GfxLCD"""
    def __init__(self, gfxlcd, lcd_flush=False):
        """Class init"""
        self.gfxlcd = gfxlcd
        self.mode = 0
        self.initialized = False
        self.lcd_flush = lcd_flush
        self.font = self.gfxlcd.options['font']
        self.width = self.gfxlcd.width // self.font.size[0]
        self.height = self.gfxlcd.height // self.font.size[1]
        self.pins = {
            'E2': None
        }
        self.position = {
            'x': 0,
            'y': 0
        }
        self.address = []

    def init(self):
        """init function"""
        if self.initialized:
            return
        for address in range(self.height):
            self.address.append(100 + (address * self.width))

        self.gfxlcd.init()
        self.initialized = True

    def cmd(self, char, enable=0):
        """write command - set cursor position"""
        if char < 100:
            return
        char -= 100
        pos_y = char // self.width
        pos_x = char - (pos_y * self.width)
        self.position = {
            'x': pos_x * self.font.size[0],
            'y': pos_y * self.font.size[1]
        }

    def shutdown(self):
        """shutdown procedure"""
        pass

    def send(self, enable=0):
        """send ack command"""
        pass

    def write(self, char, enable=0):
        """write data to lcd"""
        pass

    def char(self, char, enable=0):
        """write char to lcd"""
        self.gfxlcd.draw_text(
            self.position['x'], self.position['y'], char, True
        )
        self._increase_x()

    def set_mode(self, mode):
        """sets driver mode. 4/8 bit"""
        self.mode = mode

    def _increase_x(self):
        self.position['x'] += self.font.size[0]

    def get_line_address(self, idx):
        return self.address[idx]

    def pre_flush(self, buffer):
        pass

    def post_flush(self, buffer):
        """called after flush()"""
        if self.lcd_flush:
            self.gfxlcd.flush(True)
