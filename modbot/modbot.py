import os
import yaml
from dotbot.config import ConfigReader
from dotbot.dispatcher import Dispatcher


def add(config_file, filename, target=None):
    home = os.getenv('HOME')
    dotfiles = os.getenv('DOTFILES')
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)
    config_path, config_file = os.path.split(config_file)

    if not target_path:
        target_path = dotfiles

    if not config_path:
        config_path = dotfiles

    config = _read_config(config_file)
    i = [i for i, d in enumerate(config) if 'link' in d][0]
    filename = os.path.join(path.replace(home, '~'), filename)
    target = os.path.join(target_path.replace(dotfiles, ''), target)
    config_file = os.path.join(config_path, config_file)
    config[i]['link'][filename] = target

    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    dispatcher = Dispatcher(os.getcwd())
    dispatcher.dispatch(config)


def _read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()
