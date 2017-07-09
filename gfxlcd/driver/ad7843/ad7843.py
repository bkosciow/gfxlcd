"""Driver for AD7843 touch panel"""
import RPi.GPIO  # pylint: disable=I0011,F0401
from gfxlcd.abstract.touch import Touch


class AD7843(Touch):
    """AD7843 class"""
    def __init__(self, width, height, int_pin=None,
                 callback=None, cs_pin=None, spi=0, speed=1000000):
        super().__init__(width, height, int_pin, callback, cs_pin, spi, speed)
        self.correction = {
            'x': 364,
            'y': 430,
            'ratio_x': 14.35,
            'ratio_y': 10.59
        }

    def _get_xy(self, offset_x, offset_y):
        """correct x and y"""
        if self.rotate == 0:
            return int(
                (offset_x - self.correction['x']) / self.correction['ratio_x']
            ), int(
                (offset_y - self.correction['y']) / self.correction['ratio_y']
            )

        if self.rotate == 90:
            return self.height - int(
                (offset_y - self.correction['y']) / self.correction['ratio_y']
            ), int(
                (offset_x - self.correction['x']) / self.correction['ratio_x']
            )

        if self.rotate == 180:
            return self.width - int(
                (offset_x - self.correction['x']) / self.correction['ratio_x']
            ), self.height - int(
                (offset_y - self.correction['y']) / self.correction['ratio_y']
            )

        if self.rotate == 270:
            return int(
                (offset_y - self.correction['y']) / self.correction['ratio_y']
            ), self.width - int(
                (offset_x - self.correction['x']) / self.correction['ratio_x']
            )

    def get_position(self):
        """get touch coords"""
        buffer = []
        fuse = 40
        while len(buffer) < 20 and fuse > 0:
            if self.cs_pin:
                RPi.GPIO.output(self.cs_pin, 0)
            self.spi.xfer2([0xd0])
            recvx = self.spi.readbytes(2)
            self.spi.xfer2([0x90])
            recvy = self.spi.readbytes(2)
            if self.cs_pin:
                RPi.GPIO.output(self.cs_pin, 1)

            tc_rx = recvx[0] << 5
            tc_rx |= recvx[1] >> 3

            tc_ry = recvy[0] << 5
            tc_ry |= recvy[1] >> 3

            pos_x, pos_y = self._get_xy(tc_rx, tc_ry)
            if self._in_bounds(pos_x, pos_y):
                buffer.append((pos_x, pos_y))
            fuse -= 1

        return self._calculate_avr(buffer)
