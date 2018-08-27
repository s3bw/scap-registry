import os
import random
import string
import unittest


os.environ['APP_ENV'] = 'test'


import scap_registry  # noqa: E402


class TestCase(unittest.TestCase):

    def setUp(self):
        scap_registry.app.testing = True
        self.app = scap_registry.app.test_client()

    def generate_note_id(self, length=8):
        return ''.join([random.choice(string.ascii_uppercase + string.digits)
                        for x in range(length)])
