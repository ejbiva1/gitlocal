import json
from datetime import date, datetime
from decimal import Decimal


class JsonExtendEncoder(json.JSONEncoder):
    """
    This class provide an extension to json serialization for datetime/date.
    python json package has some methods to serialze variables, especially json.JSONEncoder.default()
    """

    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, Decimal):
            return o.__str__()
        else:
            return json.JSONEncoder.default(self, o)


class ResponseModel:
    # result
    data = []

    # status => error code
    code = '0'

    # message

    message = 'success'

    def __init__(self, data, code, message):
        self.data = data;
        self.code = code;
        self.message = message;
