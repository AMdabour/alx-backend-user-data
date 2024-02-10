#!/usr/bin/env python3
"""filtering function"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returnig the log message obfuscated"""
    pattern = fr'(?P<field>{"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, fr'\g<field>={redaction}', message)
