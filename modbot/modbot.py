import os
import yaml
from dotbot.config import ConfigReader
from dotbot.dispatcher import Dispatcher


def add(config_file, filename, target=None):
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)
    config_path, config_file = os.path.split(config_file)

    if not target_path:
        target_path = os.getenv('DOTFILES')

    if not config_path:
        config_path = os.getenv('DOTFILES')

    config = _read_config(config_file)
    i = [i for i, d in enumerate(config) if 'link' in d][0]
    config[i]['link'][filename] = target if target else filename

    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    dispatcher = Dispatcher(os.getcwd())
    dispatcher.dispatch(config)


def _read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()
