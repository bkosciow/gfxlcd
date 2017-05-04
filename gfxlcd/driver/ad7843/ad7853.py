import spidev  # pylint: disable=I0011,F0401


class AD7843(object):
    """AD7843 class"""
    def __init__(self, width, height, spi=0):
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

    def get_x(self, value):
        """correct value to x"""
        return self.width - int((value - self.correction['x']) / self.correction['ratio_x'])

    def get_y(self, value):
        """correct value to y"""
        return self.height - int((value - self.correction['y']) /  self.correction['ratio_y'])

    def get_position(self):
        """get touch coords"""
        buffer = []
        while len(buffer) < 20:
            self.spi.xfer2([0xd0])
            rx = self.spi.readbytes(2)
            self.spi.xfer2([0x90])
            ry = self.spi.readbytes(2)

            tc_rx = rx[0] << 5
            tc_rx |= rx[1] >> 3

            tc_ry = ry[0] << 5
            tc_ry |= ry[1] >> 3

            x = self.get_x(tc_rx)
            y = self.get_y(tc_ry)
            if x < 0 or x > self.width or y < 0 or y > self.height:
                return None
            buffer.append((x, y))

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
        """vlose action"""
        self.spi.close()

