import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO


class AD7843(object):
    """AD7843 class"""
    def __init__(self, width, height, int_pin=None, callback=None, spi=0):
        self.width = width
        self.height = height
        self.spi = spidev.SpiDev()
        self.spi.open(spi, 0)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 0
        self.correction = {
            'x': 364,
            'y': 430,
            'ratio_x': 14.35,
            'ratio_y': 10.59
        }
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

    def get_x(self, value):
        """correct value to x"""
        return self.width - int((value - self.correction['x']) / self.correction['ratio_x'])

    def get_y(self, value):
        """correct value to y"""
        return self.height - int((value - self.correction['y']) / self.correction['ratio_y'])

    def _interrupt(self, channel):
        """call users callback"""
        self.callback(self.get_position())

    def get_position(self):
        """get touch coords"""
        buffer = []
        while len(buffer) < 20:
            self.spi.xfer2([0xd0])
            recvx = self.spi.readbytes(2)
            self.spi.xfer2([0x90])
            recvy = self.spi.readbytes(2)

            tc_rx = recvx[0] << 5
            tc_rx |= recvx[1] >> 3

            tc_ry = recvy[0] << 5
            tc_ry |= recvy[1] >> 3

            pos_x = self.get_x(tc_rx)
            pos_y = self.get_y(tc_ry)
            if  0 <= pos_x <= self.width and 0 <= pos_y <= self.height:
                buffer.append((pos_x, pos_y))

        return self._calculate_avr(buffer)

    def _calculate_avr(self, points):
        """calculate x,y by average"""
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

