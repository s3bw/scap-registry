from flask import request
from flask import Response

from scap_lib import storage

from .app import app
from .utils import response
from .utils import api_error


store = storage.load()


@app.route('/v1/notes/<note_id>', methods=['GET'])
def get_note_content(note_id):
    try:
        return store.get_content(store.note_content_path(note_id))
        # return Response(store.stream_read(store.note_content_path(
        #     note_id)))
    except IOError:
        return api_error('Image not found', 404)


@app.route('/v1/notes/<note_id>', methods=['PUT'])
def put_note_content(note_id):
    store.stream_write(store.note_content_path(note_content_path),
        request.stream)
    return response()
