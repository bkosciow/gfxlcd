"""Common drawing functions"""
import math


class Pixel(object):
    """Pixel class"""
    def __init__(self, driver):
        self.driver = driver
        self.rotation = 0
        self.options['color'] = {
            'R': 255, 'G': 255, 'B': 255
        }
        self.options['background_color'] = {
            'R': 0, 'G': 0, 'B': 0,
        }
        self.options['threshold'] = 50
        self.options['transparency_color'] = None

    @property
    def threshold(self):
        """get threshold for B&W conversion"""
        return self.options['threshold']

    @threshold.setter
    def threshold(self, threshold):
        """set B&W threshold for conversion """
        self.options['threshold'] = threshold

    @property
    def transparency_color(self):
        """get transparency color"""
        return self.options['transparency_color']

    @transparency_color.setter
    def transparency_color(self, transparency_color):
        """set transparency color """
        self.options['transparency_color'] = transparency_color

    def draw_pixel(self, pos_x, pos_y):
        """dummy function"""
        pass

    def draw_line(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """dummy function"""
        pass

    def draw_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """draw a rectangle"""
        self.draw_line(pos_x1, pos_y1, pos_x2, pos_y1)
        self.draw_line(pos_x1, pos_y2, pos_x2, pos_y2)
        self.draw_line(pos_x1, pos_y1, pos_x1, pos_y2)
        self.draw_line(pos_x2, pos_y1, pos_x2, pos_y2)

    def draw_circle(self, pos_x, pos_y, radius):
        """draw a circle"""
        err = 0
        offset_x = radius
        offset_y = 0
        while offset_x >= offset_y:
            self.draw_pixel(pos_x + offset_x, pos_y + offset_y)
            self.draw_pixel(pos_x + offset_y, pos_y + offset_x)
            self.draw_pixel(pos_x - offset_y, pos_y + offset_x)
            self.draw_pixel(pos_x - offset_x, pos_y + offset_y)
            self.draw_pixel(pos_x - offset_x, pos_y - offset_y)
            self.draw_pixel(pos_x - offset_y, pos_y - offset_x)
            self.draw_pixel(pos_x + offset_y, pos_y - offset_x)
            self.draw_pixel(pos_x + offset_x, pos_y - offset_y)
            if err <= 0:
                offset_y += 1
                err += 2*offset_y + 1
            else:
                offset_x -= 1
                err -= 2*offset_x + 1

    def draw_arc(self, pos_x, pos_y, radius, start, end):
        """draw an arc"""
        start = start * math.pi / 180
        end = end * math.pi / 180

        err = 0
        offset_x = radius
        offset_y = 0
        while offset_x >= offset_y:
            if start <= math.atan2(offset_y, offset_x) <= end:
                self.draw_pixel(pos_x + offset_x, pos_y + offset_y)
            if start <= math.atan2(offset_x, offset_y) <= end:
                self.draw_pixel(pos_x + offset_y, pos_y + offset_x)
            if start <= math.atan2(offset_x, -offset_y) <= end:
                self.draw_pixel(pos_x - offset_y, pos_y + offset_x)
            if start <= math.atan2(offset_y, -offset_x) <= end:
                self.draw_pixel(pos_x - offset_x, pos_y + offset_y)

            if start <= math.atan2(-offset_y, -offset_x) + 2*math.pi <= end:
                self.draw_pixel(pos_x - offset_x, pos_y - offset_y)
            if start <= math.atan2(-offset_x, -offset_y) + 2*math.pi <= end:
                self.draw_pixel(pos_x - offset_y, pos_y - offset_x)
            if start <= math.atan2(-offset_x, offset_y) + 2*math.pi <= end:
                self.draw_pixel(pos_x + offset_y, pos_y - offset_x)
            if start <= math.atan2(-offset_y, offset_x) + 2*math.pi <= end:
                self.draw_pixel(pos_x + offset_x, pos_y - offset_y)

            if err <= 0:
                offset_y += 1
                err += 2*offset_y + 1
            else:
                offset_x -= 1
                err -= 2*offset_x + 1

    def _calculate_line_steps(self, length, step, required_length):
        """calculate lineparts - helper"""
        steps = [length for _ in range(0, step)]
        if step * length < required_length:
            offset = len(steps) // 2
            rest = required_length - step * length
            steps_even = True if len(steps) & 1 == 0 else False
            rest_even = True if rest & 1 == 0 else False
            appendix = 0
            for idx in range(0, rest):
                steps[offset + appendix] += 1
                if steps_even:
                    appendix = self._calculate_line_appendix(appendix)
                elif idx > 0 and rest_even:
                    appendix = self._calculate_line_appendix(appendix)
                elif not rest_even:
                    appendix = self._calculate_line_appendix(appendix)

        return steps

    def _calculate_line_appendix(self, appendix):
        """calculate appendix during drawing a line"""
        if appendix == 0:
            appendix = -1
        elif appendix < 0:
            appendix *= -1
        else:
            appendix = (appendix + 1) * -1

        return appendix

    def draw_text(self, pos_x, pos_y, text):
        """draw a text"""
        font = self.options['font']
        idx = 0
        for letter in text:
            self._draw_letter(pos_x + idx, pos_y, letter)
            idx += font.size[0]

    def _draw_letter(self, pos_x, pos_y, letter):
        """draw a letter"""
        font = self.options['font']
        bits = font.size[0]
        for row, data in enumerate(font.get(letter)):
            for bit in range(bits):
                if data & 0x01:
                    self.draw_pixel(pos_x + bit, pos_y + row)
                data >>= 1

