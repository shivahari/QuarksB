"""
Base Helper Object
"""
from loguru import logger

class BaseHelper():
    """
    Base class object for other helpers
    """

    def __init__(self):
        "Initialize base class"
        self.logger = logger

    def write(self, msg, level='info'):
        "Write log message"
        try:
            if level == 'info':
                self.logger.info(msg)
            elif level == 'error':
                self.logger.error(msg)
        except Exception as err:
            self.logger.error(f'Unable to write log messages, due to {err}')
