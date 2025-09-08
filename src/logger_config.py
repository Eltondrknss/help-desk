import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logger():
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s (%(filename)s:%(lineno)d)"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    app_log_handler = RotatingFileHandler(
        'app.log', maxBytes = 10*1024*1024, backupCount = 5, encoding = 'utf-8'
    )
    app_log_handler.setFormatter(log_formatter)
    app_log_handler.setLevel(logging.INFO)

    error_log_handler = RotatingFileHandler(
        'error.log', maxBytes = 5*1024*1024, backupCount = 5, encoding = 'utf-8'
    )

    error_log_handler.setFormatter(log_formatter)
    error_log_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    root_logger.addHandler(app_log_handler)
    root_logger.addHandler(error_log_handler)
    root_logger.addHandler(console_handler)