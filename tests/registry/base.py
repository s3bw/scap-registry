import os
import random
import string
import unittest
import shutil


os.environ['APP_ENV'] = 'test'

import scap_registry  # noqa: E402


class TestCase(unittest.TestCase):
    #: allocate variable for a temp folder
    tmp_folder = None

    def setUp(self):
        scap_registry.app.testing = True
        self.app = scap_registry.app.test_client()

    def generate_note_id(self, length=8):
        """Generate note id and save it as temp folder name."""
        self.tmp_folder = ''.join([
            random.choice(string.ascii_uppercase + string.digits)
            for x in range(length)
        ])
        return self.tmp_folder

    def tearDown(self):
        # If temp folder has been created, remove it
        if self.tmp_folder:
            shutil.rmtree('/tmp/test/notes/' + self.tmp_folder)
