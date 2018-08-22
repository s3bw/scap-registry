import re
import os


VAR_PATTERN = '\${([A-Z]+)}'


def path_vars(path):
    """Insert the environment variables in path strings.
    """
    env_vars = re.findall(VAR_PATTERN, path)
    for key in env_vars:
        value = os.environ.get(key)
        path = path.replace("${" + key + "}", value)
    return path


if __name__ == '__main__':
    path = "${HOME}/.fscap_cloud_test"
    assert path_vars(path) == "/home/sebastien/.fscap_cloud_test"
