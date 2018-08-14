import json
from datetime import datetime

import requests


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


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


file_name = 'fake_note'
data = mock_data(3)
json_dump = json.dumps(
    data,
    indent=4,
    sort_keys=True,
    cls=DateTimeEncoder)

print(json_dump)

stream_data = open(file_name, 'rb')

# Post content
requests.put(
    'http://localhost:5000/v1/notes/{}/content'.format(file_name),
    data=stream_data
)
# Post meta data
requests.put(
    'http://localhost:5000/v1/notes/{}/json'.format(file_name),
    data=json_dump
)

# Get all meta data
requests.get(
    'http://localhost:5000/v1/meta_data/load',
)

stream_data.close()
