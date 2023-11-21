from enum import Enum
from datetime import datetime

class MessageType(Enum):
    LOADING = 'LOADING'
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'

def format_currency(value):
    return "{:,.0f} VND".format(value).replace(',', '.')

def format_datetime(value):
    return value.strftime("%d/%m/%Y, %H:%M")