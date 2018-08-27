import json

from flask import request
from flask import Response

from scap_lib import storage

from .app import app
from .utils import response
from .utils import api_error
from .utils import DateTimeDecoder


store = storage.load()


@app.route('/v1/notes/<note_id>/content', methods=['GET'])
def get_note_content(note_id):
    try:
        return store.get_content(store.note_content_path(note_id))
    except IOError:
        return api_error('Note not found', 404)


@app.route('/v1/notes/<note_id>/content', methods=['PUT'])
def put_note_content(note_id):
    store.stream_write(store.note_content_path(note_id),
        request.stream)
    return response()


@app.route('/v1/notes/<note_id>/json', methods=['GET'])
def get_note_json(note_id):
    data = None
    try:
        data = store.get_content(store.note_json_path(note_id))
    except IOError:
        return api_error('Note not found', 404)
    return response(data)


@app.route('/v1/notes/<note_id>/json', methods=['PUT'])
def put_note_json(note_id):
    store.stream_write(store.note_json_path(note_id),
        request.stream)
    return response()


@app.route('/v1/meta_data/load', methods=['GET'])
def get_meta_data():
    all_data = {}
    for f in store.list_directory('notes'):
        key = f.split('/')[1]
        value = store.get_content(store.note_json_path(key))
        all_data.update(
            {key: json.loads(value)}
        )
    return response(all_data)
