import logging
import os


def setup_logger(logger_name: str) -> logging.Logger:
    """Configure logging using simplified formatting"""

    logger = logging.getLogger(logger_name)
    loglevel = os.getenv("LOGLEVEL", "INFO")

    logger.setLevel(getattr(logging, loglevel))

    # change logging format for root logger handler
    root = logging.getLogger()
    formatter = logging.Formatter("'%(levelname)-8s - %(name)s - %(module)s - Line %(lineno)d : %(message)s'\n")
    try:
        root.handlers[0].setFormatter(formatter)
    except IndexError:
        print("Failed updating default formatter for root logger")

    return logger