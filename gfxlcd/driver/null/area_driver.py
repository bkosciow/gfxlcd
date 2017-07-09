"""Area driver """
from gfxlcd.abstract.driver import Driver


class AreaDriver(Driver):
    """Null communication driver"""
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.buffer = [[0] * self.height for x in range(self.width)]
        self.area = {
            'start_x': 0,
            'start_y': 0,
            'end_x': width,
            'end_y': height
        }
        self.pointer = (0, 0)

    def init(self):
        """initialize pins"""
        pass

    def reset(self):
        """reset a display"""
        pass

    def cmd(self, data, enable):
        """send command to display"""
        pass

    def data(self, data, enable):
        """send data to display"""
        app_x, app_y = self.pointer
        self.buffer[
            self.area['start_x'] + app_x][self.area['start_y'] + app_y
        ] = data
        self._inc_pointer()

    def _inc_pointer(self):
        app_x, app_y = self.pointer
        app_x += 1
        if self.area['start_x'] + app_x > self.area['end_x']:
            app_x = 0
            app_y += 1

        if self.area['start_y'] + app_y > self.area['end_y']:
            app_x = 0
            app_y = 0

        self.pointer = (app_x, app_y)
