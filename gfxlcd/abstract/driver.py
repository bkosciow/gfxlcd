"""Interface for communication driver"""
import abc


class Driver(metaclass=abc.ABCMeta):
    """Driver interface"""
    @abc.abstractmethod
    def init(self):
        """initialize a device"""
        pass

    @abc.abstractmethod
    def reset(self):
        """resets a device"""
        pass

    @abc.abstractmethod
    def cmd(self, data, enable):
        """sends command to device"""
        pass

    @abc.abstractmethod
    def data(self, data, enable):
        """sends data to device"""
        pass
