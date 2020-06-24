import os
import logging


def __set_logger():
    _logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    if os.getenv("LOG_LEVEL", "info") == "debug":
        _logger.setLevel(logging.DEBUG)
    elif os.getenv("LOG_LEVEL", "info") == "info":
        _logger.setLevel(logging.INFO)

    return _logger


logger = __set_logger()
