import os

import yaml
from dotbot.config import ConfigReader

from modbot import DOTFILES, LOG


class Config(object):
    def __init__(self, config_file):
        config_path, config_file = os.path.split(config_file)

        if not config_path:
            config_path = DOTFILES

        self.path = config_path
        self.file = os.path.join(self.path, config_file)
        reader = ConfigReader(self.file)
        self.config = reader.get_config()
        index = [i for i, d in enumerate(self.config) if 'link' in d][0]
        self.links = self.config[index]['link']

    def add_link(self, key, value):
        if key in self.links:
            LOG.error('File already in config')
            exit(1)

        self.links[key] = os.path.relpath(value, DOTFILES)

    def remove_link(self, value):
        if value not in self.links.values():
            LOG.error('File not in config')
            exit(1)

        key = [k for (k, v) in self.links.items() if v == value][0]
        self.links.pop(key)
        return key

    def save(self):
        with open(self.file, 'w') as f:
            yaml.safe_dump(self.config, f, default_flow_style=False)
