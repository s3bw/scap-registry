import json

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
