
import logging
from logging.handlers import RotatingFileHandler



def setup_logging(logger_name: str) -> None:

    logger = logging.getLogger(logger_name)
    logger.propagate = True
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : [%(filename)s:%(lineno)s - %(funcName)s()] : %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    filehandler = RotatingFileHandler(f"logs/{logger_name}.logs", maxBytes=2000000, backupCount=20)

    filehandler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(filehandler)
