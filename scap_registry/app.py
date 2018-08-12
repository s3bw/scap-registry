"""
Just simple Key-Value storage.
"""

from flask import Flask

# import config
from .utils import response


app = Flask('scap-registry')


"""
Emailing Server Exceptions:

@app.before_first_request
def first_request():
    # cfg = config.load()
    # info = cfg.email_exceptions
"""


@app.route('/_ping')
def ping():
    return response()
