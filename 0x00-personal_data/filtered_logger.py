#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
import logging
from typing import List


PII_FIELDS = (
    "name", "email",
    "phone", "ssn",
    "password",
)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns log message with redacted details
    Args:
       fields - list of strings representing all fields to obfuscate
       redaction - string representing by what the field will be obfuscated
       message - string representing the log line
       separator - string representing by which character
                   is separating all fields in the log line (message)
    Returns:
       log message(str)
    """
    for field in fields:
        message = re.sub(r"{}=(.*?){}".format(field, separator),
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """Create a new logger for user_data"""

    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)

        return text
