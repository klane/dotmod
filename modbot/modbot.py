import os
import yaml
from dotbot.config import ConfigReader
from dotbot.dispatcher import Dispatcher


def add(config_file, filename, target=None):
    config = _read_config(config_file)
    i = [i for i, d in enumerate(config) if 'link' in d.keys()][0]
    config[i]['link'][filename] = filename if target is None else target

    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    dispatcher = Dispatcher(os.getcwd())
    dispatcher.dispatch(config)


def _read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()
