import json
from json import JSONDecoder
from datetime import datetime

from flask import current_app


def response(data=None, code=200, headers=None, raw=False):
    if data is None:
        data = True
    h = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '-1',
        'Content-Type': 'application/json'
    }
    if headers:
        h.update(headers)

    try:
        if raw is False:
            data = json.dumps(data, sort_keys=True, skipkeys=True)
    except TypeError:
        data = str(data)

    return current_app.make_response((data, code, h))


def api_error(message, code=400, headers=None):
    return response({'error': message}, code, headers)


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        # Using JSONDecoder in two different ways
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    def dict_to_object(self, d):
        if '__type__' not in d:
            return d
        _type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = _type
            return d
