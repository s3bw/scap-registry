import io
import json

import base


class TestNotes(base.TestCase):
    """Notes and content are first PUT
        then we GET.
    """

    def test_note_content(self):
        """Test note content GET and PUT."""
        note_id = self.generate_note_id()
        endpoint = "/v1/notes/{}/content".format(note_id)
        text = ("My test note content"
                "Super ordinary text.")
        stream_file = io.StringIO(text)

        resp = self.app.put(endpoint, data=stream_file)
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get(endpoint)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), text)

    def test_note_json(self):
        note_id = self.generate_note_id()
        json_data = json.dumps({'id': note_id})
        endpoint = "/v1/notes/{}/json".format(note_id)

        result = self.app.put(endpoint, data=json_data)
        self.assertEqual(result.status_code, 200)

        resp = self.app.get(endpoint)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data.decode()), json_data)

    def test_get_meta_data(self):
        note_id = self.generate_note_id()
        json_data = json.dumps({'id': note_id})
        endpoint = "/v1/notes/{}/json".format(note_id)
        result = self.app.put(endpoint, data=json_data)
        self.assertEqual(result.status_code, 200)

        # Test meta_data endpoint
        end_point = "/v1/meta_data/load"
        result = self.app.get(end_point)
        self.assertEqual(result.status_code, 200)

        expected_data = {note_id: {'id': note_id}}
        self.assertEqual(json.loads(result.data.decode()), expected_data)

    def test_delete_note(self):
        note_id = self.generate_note_id()
        json_data = json.dumps({'id': note_id})
        endpoint = "/v1/notes/{}/json".format(note_id)
        result = self.app.put(endpoint, data=json_data)
        self.assertEqual(result.status_code, 200)

        # Test delete note endpoint
        endpoint = '/v1/notes/{}'.format(note_id)
        self.app.delete(endpoint)

        result = self.app.get('/v1/notes/{}/content'.format(note_id))
        self.assertEqual(result.status_code, 404)
        self.tmp_folder = None

    def test_note_not_found(self):
        resp = self.app.get('/v1/notes/NOTFOUND/content')
        self.assertEqual(resp.status_code, 404)

    def test_note_not_found_json(self):
        resp = self.app.get('/v1/notes/NOTFOUND/json')
        self.assertEqual(resp.status_code, 404)
