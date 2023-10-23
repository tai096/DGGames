from enum import Enum
class MessageType(Enum):
    LOADING = 'LOADING'
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'

def format_currency(value):
    return "{:,.0f} VND".format(value).replace(',', '.')