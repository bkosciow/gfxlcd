"""XPT2046 touch pabel driver"""
import RPi.GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.touch import Touch


class XPT2046(Touch):
    """XPT2046 class"""
    def __init__(self, width, height, int_pin=None, callback=None, cs_pin=None, spi=0, speed=1000000):
        super().__init__(width, height, int_pin, callback, cs_pin, spi, speed)
        self.correction = {
            'x': 540,
            'y': 50,
            'ratio_x': 0.94,
            'ratio_y': 1.26,
        }

    def _get_xy(self, offset_x, offset_y):
        """correct x and y"""
        if self.rotate == 0:
            return int((offset_x - self.correction['x']) / self.correction['ratio_x']), \
                self.height - int((offset_y - self.correction['y']) / self.correction['ratio_y'])

        if self.rotate == 90:
            return int((offset_y - self.correction['y']) / self.correction['ratio_y']), \
                int((offset_x - self.correction['x']) / self.correction['ratio_x']),

        if self.rotate == 180:
            return self.width - int((offset_x - self.correction['x']) / self.correction['ratio_x']), \
                int((offset_y - self.correction['y']) / self.correction['ratio_y'])

        if self.rotate == 270:
            return self.height - int((offset_y - self.correction['y']) / self.correction['ratio_y']), \
                self.width - int((offset_x - self.correction['x']) / self.correction['ratio_x'])

    def get_position(self):
        """get touch coords"""
        buffer = []
        fuse = 40
        while len(buffer) < 20 and fuse > 0:
            if self.cs_pin:
                RPi.GPIO.output(self.cs_pin, 0)

            self.spi.xfer2([0x80 | 0x08 | 0x30])
            recv = self.spi.readbytes(1)
            tc_rz = recv[0] & 0x7f

            self.spi.xfer2([0x80 | 0x08 | 0x40])
            recv = self.spi.readbytes(1)
            tc_rz += (255-recv[0] & 0x7f)

            self.spi.xfer2([0x80 | 0x10])
            recv = self.spi.readbytes(2)
            tc_rx = 1023-((recv[0] << 2)|(recv[1] >> 6))

            self.spi.xfer2([0x80 | 0x50])
            recv = self.spi.readbytes(2)
            tc_ry = ((recv[0] << 2)|(recv[1] >> 6))

            if self.cs_pin:
                RPi.GPIO.output(self.cs_pin, 1)
            if tc_rz > 10:
                pos_x, pos_y = self._get_xy(tc_rx, tc_ry)
                if self._in_bounds(pos_x, pos_y):
                    buffer.append((pos_x, pos_y))
            fuse -= 1

        return self._calculate_avr(buffer)
