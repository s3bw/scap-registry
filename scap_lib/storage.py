import os
from io import StringIO

# import config


ROOT_PATH = "/home/sebastien/.fscap_notes_dev"


class Storage:
    """ Storage is organized as follows:
    $ROOT/notes/<note_id>
    $ROOT/data/note_data.pkl
    """

    notes = 'notes'
    buffer_size = 4096

    def note_data_path(self):
        return 'data/note_data.pkl'

    def note_content_path(self, note_id):
        return '{0}/{1}'.format(self.notes, note_id)

    def get_content(self, path):
        raise NotImplemented

    def put_content(self, path, content):
        raise NotImplemented

    def stream_read(self, path):
        raise NotImplemented

    def stream_write(self, path, fp):
        raise NotImplemented

    def list_directory(self, path=None):
        raise NotImplemented

    def exists(self, path):
        raise NotImplemented

    def remove(self, path):
        raise NotImplemented


class LocalStorage(Storage):

    def __init__(self):
        # self._config = config.load()
        # self._root_path = self._config.storage_path
        self._root_path = ROOT_PATH

    def _init_path(self, path=None, create=False):
        path = os.path.join(self._root_path, path) if path else self._root_path
        if create is True:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        return path

    def get_content(self, path, html=True):
        path = self._init_path(path)
        with open(path, mode='r') as f:
            if html:
                return '<br>'.join(f.readlines())
            else f.read()

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
        if os.path.isdir(path):
            os.rmdir(path)
            return
        os.remove(path)


def load(kind=None):
    """Returns the appropriate storage class.
    """
    # if kind == 'local':
    store = LocalStorage()
    return store
