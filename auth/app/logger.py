import os
import logging


def __set_logger():
    _logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return _logger


logger = __set_logger()
