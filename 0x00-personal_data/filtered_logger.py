#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
from typing import List


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
