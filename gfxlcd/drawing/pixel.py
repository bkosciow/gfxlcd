"""Common drawing functions"""
import math


class Pixel(object):
    """Pixel class"""
    def __init__(self, driver):
        self.options['color'] = {
            'R': 255, 'G': 255, 'B': 255
        }
        self.options['background_color'] = {
            'R': 0, 'G': 0, 'B': 0,
        }

    def draw_pixel(self, pos_x, pos_y):
        """dummy fuction"""
        pass

    def draw_line(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """dummy fuction"""
        pass

    def draw_rect(self, x1, y1, x2, y2):
        """draw a rectangle"""
        self.draw_line(x1, y1, x2, y1)
        self.draw_line(x1, y2, x2, y2)
        self.draw_line(x1, y1, x1, y2)
        self.draw_line(x2, y1, x2, y2)

    def draw_circle(self, x, y, radius):
        """draw a circle"""
        err = 0
        offset_x = radius
        offset_y = 0
        while offset_x >= offset_y:
            self.draw_pixel(x + offset_x, y + offset_y)
            self.draw_pixel(x + offset_y, y + offset_x)
            self.draw_pixel(x - offset_y, y + offset_x)
            self.draw_pixel(x - offset_x, y + offset_y)
            self.draw_pixel(x - offset_x, y - offset_y)
            self.draw_pixel(x - offset_y, y - offset_x)
            self.draw_pixel(x + offset_y, y - offset_x)
            self.draw_pixel(x + offset_x, y - offset_y)
            if err <= 0:
                offset_y += 1
                err += 2*offset_y + 1
            else:
                offset_x -= 1
                err -= 2*offset_x + 1

    def draw_arc(self, x, y, radius, start, end):
        """draw an arc"""
        start = start * math.pi / 180
        end = end * math.pi / 180

        err = 0
        offset_x = radius
        offset_y = 0
        while offset_x >= offset_y:
            if start <= math.atan2(offset_y, offset_x) <= end:
                self.draw_pixel(x + offset_x, y + offset_y)
            if start <= math.atan2(offset_x, offset_y) <= end:
                self.draw_pixel(x + offset_y, y + offset_x)
            if start <= math.atan2(offset_x, -offset_y) <= end:
                self.draw_pixel(x - offset_y, y + offset_x)
            if start <= math.atan2(offset_y, -offset_x) <= end:
                self.draw_pixel(x - offset_x, y + offset_y)

            if start <= math.atan2(-offset_y, -offset_x) + 2*math.pi <= end:
                self.draw_pixel(x - offset_x, y - offset_y)
            if start <= math.atan2(-offset_x, -offset_y) + 2*math.pi <= end:
                self.draw_pixel(x - offset_y, y - offset_x)
            if start <= math.atan2(-offset_x, offset_y) + 2*math.pi <= end:
                self.draw_pixel(x + offset_y, y - offset_x)
            if start <= math.atan2(-offset_y, offset_x) + 2*math.pi <= end:
                self.draw_pixel(x + offset_x, y - offset_y)

            if err <= 0:
                offset_y += 1
                err += 2*offset_y + 1
            else:
                offset_x -= 1
                err -= 2*offset_x + 1
