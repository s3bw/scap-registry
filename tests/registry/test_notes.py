import io
import json

import base


class TestNotes(base.TestCase):

    def test_note_content(self):
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

    def test_note_not_found(self):
        resp = self.app.get('/v1/notes/NOTFOUND/content')
        self.assertEqual(resp.status_code, 404)

    def test_note_not_found_json(self):
        resp = self.app.get('/v1/notes/NOTFOUND/json')
        self.assertEqual(resp.status_code, 404)
