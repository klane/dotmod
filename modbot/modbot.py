import os
import sys
import dotbot
import yaml
from dotbot.config import ConfigReader
from dotbot.messenger import Messenger

HOME = os.getenv('HOME')
DOTFILES = os.getenv('DOTFILES')


def add(config_file, filename, target=None):
    log = Messenger()
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)
    config_path, config_file = os.path.split(config_file)

    if not config_path:
        config_path = DOTFILES

    if not target_path:
        target_path = config_path
    elif config_path not in target_path:
        target_path = os.path.join(config_path, target_path)

    fullfile = os.path.join(path.replace(HOME, '~'), filename)
    target = os.path.join(target_path, target)
    config_file = os.path.join(config_path, config_file)
    config = _read_config(config_file)
    i = [i for i, d in enumerate(config) if 'link' in d][0]

    if fullfile in config[i]['link']:
        log.error('File already in config')
        exit(1)

    if not os.path.isfile(os.path.join(path, filename)):
        log.error('File does not exist')
        exit(1)

    if os.path.isfile(target):
        log.error('File already linked')
        exit(1)

    config[i]['link'][fullfile] = target.replace(DOTFILES + os.sep, '')

    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    log.info('Moving {0} from {1} to {2}'.format(filename, path, target_path))
    os.rename(os.path.join(path, filename), target)
    sys.argv[1:] = ['--config-file', config_file]
    dotbot.main()


def _read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()
