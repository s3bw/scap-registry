# flake8: noqa
import json
import argparse
from json import JSONDecoder
from json import JSONEncoder
from datetime import datetime

import requests

parser = argparse.ArgumentParser()
parser.add_argument('--port', default='5000',
                    help='Specify container/server port')
parser.add_argument('--host', default='localhost',
                    help='Specify container/server hostname')

args = parser.parse_args()

_PORT = args.port
_HOST = args.host

_FILE_NAME = 'examples/note_sample'
_FILE_ID = 'note_sample'


def mock_data(views, year=2000, tag='fake_tag', book='general'):
    modified = datetime(year, 12, 10, 15, 25, 19, 11262)
    return {
        'description': 'This is a fake note',
        'created': datetime(2000, 12, 10, 15, 25, 19, 11262),
        'modified': modified,
        'tags': [tag],
        'book': book,
        'views': views
    }


class DateTimeEncoder(JSONEncoder):
    """Encode datetime objects as a dict with a key __type__.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return JSONEncoder.default(self, obj)


"""
POST NOTE CONTENT
"""

def post_file_content(file_name, file_id):
    """In this example we can see the endpoint being used to post note
        content.
    """
    stream_data = open(file_name, 'r')
    # Post content
    requests.put(
        'http://{}:{}/v1/notes/{}/content'.format(_HOST, _PORT, file_id),
        data=stream_data
    )
    stream_data.close()


post_file_content(_FILE_NAME, _FILE_ID)

"""
GET AND PUT NOTE JSON
"""

DATA = mock_data(3)

json_dump = json.dumps(
    DATA,
    indent=4,
    sort_keys=True,
    cls=DateTimeEncoder)

# print(json_dump)

# Post JSON
requests.put(
    'http://{}:{}/v1/notes/{}/json'.format(_HOST, _PORT, _FILE_ID),
    data=json_dump
)

# Get meta data
get_json = requests.get(
    'http://{}:{}/v1/notes/{}/json'.format(_HOST, _PORT, _FILE_ID),
)
print(get_json)
print("Got Content!")

"""
ALL META DATA
"""


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


# Get all meta data
get_json = requests.get(
    'http://{}:{}/v1/meta_data/load'.format(_HOST, _PORT),
)
# Don't forget to decode!
meta_data = json.loads(get_json.content.decode(), cls=DateTimeDecoder)

print("Meta Data Tags:")
print(meta_data[_FILE_ID]['tags'])


