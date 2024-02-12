#!/usr/bin/env python3
"""filtering function"""
import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returnig the log message obfuscated"""
    pattern = fr'(?P<field>{"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, fr'\g<field>={redaction}', message)


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger('user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connection object"""
    db_user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(user=db_user,
                                         host=db_host,
                                         password=db_password,
                                         database=db_name)

    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """intitializing the class instances"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """a method for overriding the parent class format method"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)
