#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated
    
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{seperator}',
                         f'{f}={redaction}{separator}', message)
    return message
