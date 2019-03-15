import os
import sys
import dotbot
import yaml
from dotbot.config import ConfigReader
from modbot import DOTFILES, HOME, LOG


class Config(list):
    def __init__(self, config_file):
        config_path, config_file = os.path.split(config_file)

        if not config_path:
            config_path = DOTFILES

        self.path = config_path
        self.file = os.path.join(self.path, config_file)
        reader = ConfigReader(self.file)
        super(Config, self).__init__(reader.get_config())
        index = [i for i, d in enumerate(self) if 'link' in d][0]
        self.links = self[index]['link']

    def add_link(self, key, value):
        if key in self.links:
            LOG.error('File already in config')
            exit(1)

        self.links[key] = value.replace(DOTFILES + os.sep, '')

    def save(self):
        with open(self.file, 'w') as f:
            yaml.safe_dump(list(self), f, default_flow_style=False)


def add(config_file, filename, target=None):
    config = Config(config_file)
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)

    if not target_path:
        target_path = config.path
    elif config.path not in target_path:
        target_path = os.path.join(config.path, target_path)

    fullfile = os.path.join(path.replace(HOME, '~'), filename)
    target = os.path.join(target_path, target)

    if not os.path.isfile(os.path.join(path, filename)):
        LOG.error('File does not exist')
        exit(1)

    if os.path.isfile(target):
        LOG.error('File already linked')
        exit(1)

    config.add_link(fullfile, target)
    config.save()

    LOG.info('Moving {0} from {1} to {2}'.format(filename, path, target_path))
    os.rename(os.path.join(path, filename), target)
    sys.argv[1:] = ['--config-file', config.file]
    dotbot.main()
