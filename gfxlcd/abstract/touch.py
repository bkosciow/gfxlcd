"""Touch panel interface"""
import abc


class Touch(metaclass=abc.ABCMeta):
    """Touch class"""

    @abc.abstractmethod
    def init(self):
        """some additional init"""
        return

    @abc.abstractmethod
    def get_position(self):
        """returns pressed position"""
        return

    @abc.abstractmethod
    def close(self):
        """close functions"""
        return
