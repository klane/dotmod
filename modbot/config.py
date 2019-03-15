import os
import yaml
from dotbot.config import ConfigReader
from modbot import DOTFILES, LOG


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
