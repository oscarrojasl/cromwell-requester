import logging
import os.path
import sys


class Logging:
    def __init__(self, logger_name, to_file=True, to_screen=False, logger_level='DEBUG', file_level='DEBUG',
                 screen_level='ERROR', output_directory=os.path.dirname(os.path.abspath(__file__))):
        self.logger_name = logger_name
        self.to_file = to_file
        self.logger_level = logger_level
        self.to_screen = to_screen
        self.file_level = file_level
        self.screen_level = screen_level
        self.logger = None
        self.logs_dir = output_directory
        self.set_logger()

    def set_logger(self):
        self.logger = logging.getLogger(str(self.logger_name))
        self.logger.setLevel(self.logger_level)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                        '%Y-%m-%d %H:%M:%S')
        if self.to_file:
            file_handler = logging.FileHandler(filename=f'{self.logs_dir}/{self.logger_name}.log')
            file_handler.setLevel(self.file_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        if self.to_screen:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(self.screen_level)
            self.logger.addHandler(stream_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)