import logging
import sys


class LoggerConfig:
    @staticmethod
    def setup(level=logging.INFO):
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
