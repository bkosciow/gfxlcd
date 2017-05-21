import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO


class XPT2046(object):
    """XPT2046 class"""
    def __init__(self, width, height, int_pin=None, callback=None, cs_pin=None, spi=0, speed=1000000):
        self.width = width
        self.height = height
        self.spi = spidev.SpiDev()
        self.spi.open(spi, 0)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        self.correction = {
            'x': 540,
            'y': 50,
            'ratio_x': 0.94, #14.35,
            'ratio_y': 1.26, #10.59
        }
        self.cs_pin = cs_pin
        self.int_pin = int_pin
        self.callback = callback
        self.bouncetime = 500

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

    def get_x(self, value):
        """correct value to x"""
        return int((value - self.correction['x']) / self.correction['ratio_x'])

    def get_y(self, value):
        """correct value to y"""
        return int((value - self.correction['y']) / self.correction['ratio_y'])

    def _interrupt(self, channel):
        """call users callback"""
        self.callback(self.get_position())

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
                pos_x = self.get_x(tc_rx)
                pos_y = self.get_y(tc_ry)
                if 0 <= pos_x <= self.width and 0 <= pos_y <= self.height:
                    buffer.append((pos_x, pos_y))
            fuse -= 1

        return self._calculate_avr(buffer)

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

