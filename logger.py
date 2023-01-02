import logging
from config import DEBUG

#logger.log.warning(f"saved current contour")

class Singleton(type):
    """
    Singleton metaclass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):

    def __init__(self):
        """
        Set up logger
        """
        self.log = logging.getLogger()
        if DEBUG:
            self.log.setLevel(level=logging.DEBUG)
        else:
            self.log.setLevel(level=logging.INFO)
        fh = logging.StreamHandler()
        fh_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
        fh.setFormatter(fh_formatter)
        self.log.addHandler(fh)