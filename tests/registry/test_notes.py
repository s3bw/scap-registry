import io
import os
import json

import base


class TestNotes(base.TestCase):

    def test_note_content(self):
        text = (
            "My test note content"
            "Super ordinary text."
        )
        stream_file = io.StringIO(text)
        resp = self.app.put('/v1/notes/xyz/content',
            data=stream_file)
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/v1/notes/xyz/content')
        # print(str(resp.data))
        # assert False

    def test_note_json(self):
        note_id = 'xyz'
        json_data = json.dumps({
            'id': 'xxxxx',
        })

        result = self.app.put('/v1/notes/xyz/json',
            data=json_data)
        self.assertEqual(result.status_code, 200)

        resp = self.app.get('/v1/notes/xyz/json')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data.decode()), json_data)

    def test_note_not_found(self):
        resp = self.app.get('/v1/notes/NONOTEEXISTS/content')
        self.assertEqual(resp.status_code, 404)
