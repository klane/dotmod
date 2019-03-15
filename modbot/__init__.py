import os

from dotbot.messenger import Messenger

HOME = os.getenv('HOME')
DOTFILES = os.getenv('DOTFILES')
LOG = Messenger()
