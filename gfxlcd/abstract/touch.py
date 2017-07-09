"""Touch panel interface"""
import abc
import spidev  # pylint: disable=I0011,F0401
import RPi.GPIO  # pylint: disable=I0011,F0401


class Touch(metaclass=abc.ABCMeta):
    """Touch class"""
    def __init__(self, width, height, int_pin=None,
                 callback=None, cs_pin=None, spi=0, speed=1000000):
        self.width = width
        self.height = height
        self.spi = spidev.SpiDev()
        self.spi.open(spi, 0)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        self.cs_pin = cs_pin
        self.int_pin = int_pin
        self.callback = callback
        self.bouncetime = 500
        self.rotate = 0
        self.correction = {
            'x': 0,
            'y': 0,
            'ratio_x': 1,
            'ratio_y': 1,
        }

    def init(self):
        """some init functions"""
        if self.int_pin:
            RPi.GPIO.setup(self.int_pin, RPi.GPIO.IN)
            RPi.GPIO.add_event_detect(
                self.int_pin, RPi.GPIO.BOTH, callback=self._interrupt,
                bouncetime=self.bouncetime
            )
        if self.cs_pin:
            RPi.GPIO.setup(self.cs_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.cs_pin, 1)

    @abc.abstractmethod
    def get_position(self):
        """returns pressed position"""
        return

    def close(self):
        """close action"""
        if self.int_pin:
            RPi.GPIO.remove_event_detect(self.int_pin)
        self.spi.close()

    def _interrupt(self, channel):
        """call users callback"""
        self.callback(self.get_position())

    def _calculate_avr(self, points):
        """calculate x,y by average"""
        if not points:
            return None
        sum_x = 0
        sum_y = 0
        for point in points:
            sum_x += point[0]
            sum_y += point[1]

        return int(sum_x / len(points)), int(sum_y / len(points))

    def _in_bounds(self, pos_x, pos_y):
        """checks if point is in range"""
        if self.rotate == 0 or self.rotate == 180:
            return 0 <= pos_x <= self.width and 0 <= pos_y <= self.height
        return 0 <= pos_y <= self.width and 0 <= pos_x <= self.height
