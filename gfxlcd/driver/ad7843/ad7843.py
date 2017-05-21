import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO
from gfxlcd.abstract.touch import Touch


class AD7843(Touch):
    """AD7843 class"""
    def __init__(self, width, height, int_pin=None, callback=None, cs_pin=None, spi=0, speed=1000000):
        self.width = width
        self.height = height
        self.spi = spidev.SpiDev()
        self.spi.open(spi, 0)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        self.correction = {
            'x': 364,
            'y': 430,
            'ratio_x': 14.35,
            'ratio_y': 10.59
        }
        self.cs_pin = cs_pin
        self.int_pin = int_pin
        self.callback = callback
        self.bouncetime = 500
        self.rotate = 0

    def init(self):
        """some init functions"""
        if self.int_pin:
            RPi.GPIO.setup(self.int_pin, RPi.GPIO.IN)
            RPi.GPIO.add_event_detect(
                self.int_pin, RPi.GPIO.BOTH, callback=self._interrupt, bouncetime=self.bouncetime
            )
        if self.cs_pin:
            RPi.GPIO.setup(self.cs_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.cs_pin, 1)

    def _get_xy(self, offset_x, offset_y):
        """correct x and y"""
        if self.rotate == 0:
            return int((offset_x - self.correction['x']) / self.correction['ratio_x']), \
                int((offset_y - self.correction['y']) / self.correction['ratio_y'])

        if self.rotate == 90:
            return self.height - int((offset_y - self.correction['y']) / self.correction['ratio_y']), \
                int((offset_x - self.correction['x']) / self.correction['ratio_x'])

        if self.rotate == 180:
            return self.width - int((offset_x - self.correction['x']) / self.correction['ratio_x']), \
                self.height - int((offset_y - self.correction['y']) / self.correction['ratio_y'])

        if self.rotate == 270:
            return int((offset_y - self.correction['y']) / self.correction['ratio_y']), \
                self.width - int((offset_x - self.correction['x']) / self.correction['ratio_x'])

    def _interrupt(self, channel):
        """call users callback"""
        if self.cs_pin:
            RPi.GPIO.output(self.cs_pin, 0)
        self.callback(self.get_position())
        if self.cs_pin:
            RPi.GPIO.output(self.cs_pin, 1)

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

    def _in_bounds(self, pos_x, pos_y):
        """checks if point is in range"""
        if self.rotate == 0 or self.rotate == 180:
            return 0 <= pos_x <= self.width and 0 <= pos_y <= self.height
        else:
            return 0 <= pos_y <= self.width and 0 <= pos_x <= self.height

    def _calculate_avr(self, points):
        """calculate x,y by average"""
        if len(points) == 0:
            return None
        sum_x = 0
        sum_y = 0
        for point in points:
            sum_x += point[0]
            sum_y += point[1]

        return int(sum_x / len(points)), int(sum_y / len(points))

    def close(self):
        """close action"""
        if self.int_pin:
            RPi.GPIO.remove_event_detect(self.int_pin)
        self.spi.close()

