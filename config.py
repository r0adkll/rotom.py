import os
import yaml
from pathlib import Path


def load_config():
    home = str(Path.home())
    config_path = os.path.join(home, ".rotom/config.yml")
    if os.path.exists(config_path):
        stream = open(config_path, 'r')
        return yaml.load(stream)
    else:
        return {}


def load_config_from_path(path):
    if os.path.exists(path):
        stream = open(path, 'r')
        return yaml.load(stream)
    else:
        return {}
