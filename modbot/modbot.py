import os
import sys
import dotbot
import yaml
from dotbot.config import ConfigReader
from dotbot.messenger import Messenger


def add(config_file, filename, target=None):
    home = os.getenv('HOME')
    dotfiles = os.getenv('DOTFILES')
    log = Messenger()
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

    filename = os.path.join(path.replace(home, '~'), filename)
    target = os.path.join(target_path.replace(dotfiles, ''), target)
    config_file = os.path.join(config_path, config_file)
    config = _read_config(config_file)
    i = [i for i, d in enumerate(config) if 'link' in d][0]

    if filename in config[i]['link']:
        log.error('File already in config')
        exit(1)

    config[i]['link'][filename] = target

    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    if not os.path.isfile(target):
        log.info('Moving {0} from {1} to {2}'.format(filename, path, target_path))
        os.rename(filename, target)
        sys.argv[1:] = ['--config-file', config_file]
        dotbot.main()
    else:
        log.error('File already linked')
        exit(1)


def _read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()
