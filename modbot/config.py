import os

import yaml
from dotbot.config import ConfigReader

from . import DOTFILES


class Config:
    """Class to capture output from Dotbot ConfigReader"""

    def __init__(self, config_file):
        """Create Dotbot config object from .yaml file

        Args:
            config_file (str): Path to Dotbot config file
        """
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
        """Add link to Dotbot config

        Args:
            key (str): Location to which file will be linked
            value (str): Location in dotfiles repo where file will be stored
        """
        if key in self.links:
            raise ConfigError('File {} already in config'.format(key))

        self.links[key] = os.path.relpath(value, DOTFILES)

    def remove_link(self, value):
        """Remove link from Dotbot config

        Args:
            value (str): Location in dotfiles repo to remove

        Returns:
            str: Link target location
        """
        if value not in self.links.values():
            raise ConfigError('File {} not in config'.format(value))

        key = [k for (k, v) in self.links.items() if v == value][0]
        self.links.pop(key)
        return key

    def save(self):
        """Save Dotbot config file"""
        with open(self.file, 'w') as config_file:
            yaml.safe_dump(self.config, config_file, default_flow_style=False)


class ConfigError(Exception):
    """Class representing an exception with Dotbot configs"""

    pass
