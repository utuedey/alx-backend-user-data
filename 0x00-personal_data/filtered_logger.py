#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
import os
import logging
import mysql.connector
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Create a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Retrieve all rows in use table and display them"""
    
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


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
