import re
import os


VAR_PATTERN = r'\${([A-Z]+)}'


def path_vars(path):
    """Insert the environment variables in path strings.
    """
    env_vars = re.findall(VAR_PATTERN, path)
    for key in env_vars:
        value = os.environ.get(key)
        path = path.replace("${" + key + "}", value)
    return path
