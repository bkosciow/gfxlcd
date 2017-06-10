"""Font abstract"""
import abc


class Font(metaclass=abc.ABCMeta):
    font = []  # Dictionary with hex that describe each char
    size = (0, 0)

    def __init__(self):
        pass

    def get(self, letter):
        """return array with letter"""
        return self.font[ord(letter)]

    @property
    def size(self):
        """get font size"""
        return self.size
