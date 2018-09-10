import os

import yaml


class Config:

    def __init__(self, config):
        self._config = config

    def __repr__(self):
        return repr(self._config)

    def __getattr__(self, key):
        if key in self._config:
            result = self._config[key]
            if result.startswith('_env'):
                var_split = result.split(':', 2)
                var_name = var_split[1]
                var_default = '' if len(var_split) < 3 else var_split[2]
                result = os.environ.get(var_name, var_default)
            return result


_config = None


def load():
    global _config
    if _config is not None:
        return _config
    data = None
    with open(os.path.join(os.path.dirname(__file__), '..', 'config.yml')) as f:
        data = yaml.load(f)
    # Common is the config common to all flavors
    flavor = os.environ.get('APP_ENV', 'dev')
    config = data.get(flavor, {})
    _config = Config(config)
    return _config
