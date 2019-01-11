from unittest.mock import patch

from scap_lib.utils import path_vars


@patch.dict('os.environ', {'HOME': '/path/home'})
def test_path_vars():
    """Test the env args are parsed."""
    path = "${HOME}/.fscap_cloud_test"
    assert path_vars(path) == "/path/home/.fscap_cloud_test"
