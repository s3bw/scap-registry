# import urllib.request

# contents = urllib.request.urlopen("localhost:5000/v1/images/<image_id>/layer").read()


import requests

stream_data = open('readme.md', 'rb')
r = requests.put('http://localhost:5000/v1/notes/readme.md', data=stream_data)

stream_data.close()
