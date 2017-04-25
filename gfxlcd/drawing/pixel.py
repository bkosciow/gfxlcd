"""Common drawing functions"""
import math


class Pixel(object):
    """Pixel class"""
    def __init__(self, driver):
        self.driver = driver
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
