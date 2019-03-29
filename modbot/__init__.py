import os

from dotbot.messenger import Messenger

HOME = os.getenv('HOME') or os.getenv('USERPROFILE')
DOTFILES = os.getenv('DOTFILES') or os.getcwd()
LOG = Messenger()
