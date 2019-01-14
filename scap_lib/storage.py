import os
import shutil
from io import BytesIO

import boto.s3.connection
import boto.s3.key

from scap_lib import config
from scap_lib.utils import path_vars


class Storage:
    """ Storage is organized as follows:
    $ROOT/notes/<note_id>/content
    $ROOT/notes/<note_id>/json
    """

    notes = 'notes'
    buffer_size = 4096

    def note_folder(self, note_id):
        return '{0}/{1}'.format(self.notes, note_id)

    def note_content_path(self, note_id):
        return self.note_folder(note_id) + '/content'

    def note_json_path(self, note_id):
        return self.note_folder(note_id) + '/json'

    def get_content(self, path):
        raise NotImplementedError

    def put_content(self, path, content):
        raise NotImplementedError

    def stream_read(self, path):
        raise NotImplementedError

    def stream_write(self, path, fp):
        raise NotImplementedError

    def list_directory(self, path=None):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError

    def remove(self, path):
        raise NotImplementedError


class LocalStorage(Storage):

    def __init__(self):
        self._config = config.load()
        self._root_path = path_vars(self._config.storage_path)

    def _init_path(self, path=None, create=False):
        path = os.path.join(self._root_path, path) if path else self._root_path
        if create is True:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        return path

    def get_content(self, path, html=False):
        path = self._init_path(path)
        with open(path, mode='r') as f:
            if html:
                return '<br>'.join(f.readlines())
            else:
                return f.read()

    def put_content(self, path, content):
        path = self._init_path(path, create=True)
        with open(path, mode='w') as f:
            f.write(content)
        return path

    def stream_read(self, path):
        path = self._init_path(path)
        with open(path, mode='rb') as f:
            while True:
                buf = f.read(self.buffer_size)
                if not buf:
                    break
                yield buf

    def stream_write(self, path, fp):
        # Size is mandatory
        path = self._init_path(path, create=True)
        with open(path, mode='wb') as f:
            while True:
                buf = fp.read(self.buffer_size)
                if not buf:
                    break
                f.write(buf)

    def list_directory(self, path=None):
        path = self._init_path(path)
        prefix = path[len(self._root_path) + 1:] + '/'
        exists = False
        for d in os.listdir(path):
            exists = True
            yield prefix + d
        if exists is False:
            # Raises OSError even when the directory is empty
            # (to be consistent with S3)
            raise OSError('No such directory: \'{0}\''.format(path))

    def exists(self, path):
        path = self._init_path(path)
        return os.path.exists(path)

    def remove(self, path):
        path = self._init_path(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
            return
        os.remove(path)


class S3Storage(Storage):

    def __init__(self):
        self._config = config.load()
        self._s3_conn = boto.s3.connection.S3Connection(
            self._config.s3_access_key,
            self._config.s3_secret_key,
            host='s3.eu-west-2.amazonaws.com',
            is_secure=False)
        self._s3_bucket = self._s3_conn.get_bucket(self._config.s3_bucket)
        self._root_path = path_vars(self._config.storage_path)

    def _debug_key(self, key):
        """Used for debugging only."""
        orig_meth = key.bucket.connection.make_request

        def new_meth(*args, **kwargs):
            print("#" * 16)
            print(args)
            print(kwargs)
            print("#" * 16)
            return orig_meth(*args, **kwargs)
        key.bucket.connection.make_request = new_meth

    def _init_path(self, path=None):
        path = os.path.join(self._root_path, path) if path else self._root_path
        if path and path[0] == '/':
            return path[1:]
        return path

    def get_content(self, path):
        path = self._init_path(path)
        key = boto.s3.key.Key(self._s3_bucket, path)
        if not key.exists():
            raise IOError("No such key: '{}'".format(path))
        return key.get_contents_as_string().decode('utf-8')

    def put_content(self, path, content):
        path = self._init_path(path)
        key = boto.s3.key.Key(self._s3_bucket, path)
        key.set_contents_from_string(content)
        return path

    def stream_read(self, path):
        path = self._init_path(path)
        key = boto.s3.key.Key(self._s3_bucket, path)
        if not key.exists():
            raise IOError("No such key: '{}'".format(path))
        while True:
            buf = key.read(self.buffer_size)
            if not buf:
                break
            yield buf

    def stream_write(self, path, fp):
        path = self._init_path(path)
        mp = self._s3_bucket.initiate_multipart_upload(path)
        num_part = 1
        while True:
            buf = fp.read(self.buffer_size)
            if not buf:
                break
            io = BytesIO(buf)
            mp.upload_part_from_file(io, num_part)
            num_part += 1
            io.close()
        mp.complete_upload()

    def list_directory(self, path=None):
        path = self._init_path(path)
        if not path.endswith('/'):
            path += '/'
        ln = len(self._root_path)
        exists = False
        for key in self._s3_bucket.list(prefix=path, delimiter='/'):
            exists = True
            name = key.name
            if name.endswith('/'):
                yield name[ln:-1]
            else:
                yield name[ln:]
        if exists is False:
            raise OSError("No such directory: '{}'".format(path))

    def exists(self, path):
        path = self._init_path(path)
        key = boto.s3.key.Key(self._s3_bucket, path)
        return key.exists()

    def remove(self, path):
        path = self._init_path(path)
        key = boto.s3.key.Key(self._s3_bucket, path)
        if not key.exists():
            raise OSError("No such key: '{}'".format(path))
        # Does this delete folders?
        key.delete()


_storage = {}


def load(kind=None):
    """Returns the appropriate storage class.
    """
    global _storage
    if not kind:
        kind = config.load().storage.lower()
    if kind in _storage:
        return _storage[kind]

    if kind == 'local':
        store = LocalStorage()
    elif kind == 's3':
        store = S3Storage()

    _storage[kind] = store
    return store
