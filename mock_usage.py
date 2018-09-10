# flake8: noqa
import json
from json import JSONDecoder
from json import JSONEncoder
from datetime import datetime

import requests


_FILE_NAME = 'fake_note'


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

def post_file_content(file_name):
    """In this example we can see the endpoint being used to post note
        content.
    """
    stream_data = open(file_name, 'r')
    # Post content
    requests.put(
        'http://localhost:5000/v1/notes/{}/content'.format(file_name),
        data=stream_data
    )
    stream_data.close()


post_file_content(_FILE_NAME)

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
    'http://localhost:5000/v1/notes/{}/json'.format(_FILE_NAME),
    data=json_dump
)

# Get meta data
get_json = requests.get(
    'http://localhost:5000/v1/notes/{}/json'.format(_FILE_NAME),
)
# print(get_json.content)
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
    'http://localhost:5000/v1/meta_data/load',
)
# Don't forget to decode!
meta_data = json.loads(get_json.content.decode(), cls=DateTimeDecoder)

print("Meta Data Tags:")
print(meta_data['fake_note']['tags'])


