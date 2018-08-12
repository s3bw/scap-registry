# import urllib.request

# contents = urllib.request.urlopen("localhost:5000/v1/images/<image_id>/layer").read()


import requests

payload = {'file_stream': 'here'}
r = requests.put('localhost:5000/v1/image/note_name/', data=payload)
