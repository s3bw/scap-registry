import base


class TestApp(base.TestCase):

    def test_ping_status(self):
        result = self.app.get('/_ping')

        self.assertEquals(result.status_code, 200)
