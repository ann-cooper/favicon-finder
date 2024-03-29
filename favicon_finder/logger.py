import logging
import sys

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Structured logging reference: https://github.com/madzak/python-json-logger
    """

    def parse(self):
        return self._fmt.split(";")

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["status"] = log_record.get("levelname")


def get_python_version():
    """Returns the Python version in use."""
    major, minor, micro, level, serial = sys.version_info
    return float(".".join([str(major), str(minor)]))


def get_logger(name, level=logging.DEBUG, version=get_python_version()):
    """Sets up a json logger.

    Parameters
    ----------
    name : str
        The module name: `logger = logger.get_logger(__name__)`
    level : int, optional
        Set the logging level, by default logging.DEBUG
    version : int, optional
        Python version, by default get_python_version()

    Returns
    -------
    logging.Logger

    Reference
    ---------
        https://docs.python-guide.org/writing/logging/

    Note
    ----
        To print to screen and output to a txt file,
        uncomment the lines pertaining to the stream_handler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    # stream_handler = logging.StreamHandler()
    log_handler = logging.FileHandler("log.txt")
    if version >= 3.8:
        formatter = CustomJsonFormatter(
            "asctime;levelname;message;filename;lineno", validate=False
        )
    elif version == 3.7:
        formatter = CustomJsonFormatter("asctime;levelname;message;filename;lineno")
    log_handler.setFormatter(formatter)
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
    logger.addHandler(log_handler)
    logger.propagate = True
    return logger
