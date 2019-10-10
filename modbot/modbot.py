import os
import sys

import dotbot

from . import DOTFILES, HOME, LOG
from .config import Config


def add(config, filename, target=None, run=False):
    config = Config(config) if type(config) is str else config
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)

    if not target:
        target = filename

    if not target_path:
        target_path = config.path
    elif config.path not in target_path:
        target_path = os.path.join(config.path, target_path)

    filename = os.path.join(path, filename)
    target = os.path.join(target_path, target)

    if not os.path.isfile(filename):
        raise OSError('File {} does not exist'.format(filename))

    if os.path.isfile(target):
        raise OSError('File {} already linked'.format(filename))

    config.add_link(filename.replace(HOME, '~'), target)
    config.save()
    notify(filename, target)
    os.rename(filename, target)

    if run:
        run_dotbot(config.file)


def remove(config, filename, run=False):
    config = Config(config) if type(config) is str else config

    if config.path not in filename:
        filename = os.path.join(config.path, filename)

    if not os.path.isfile(filename):
        raise OSError('File {} not in repo'.format(filename))

    link_display = config.remove_link(os.path.relpath(filename, DOTFILES))
    link = link_display.replace('~', HOME)

    if not os.path.isfile(link):
        raise OSError('Link {} does not exist'.format(link_display))

    config.save()
    notify(filename, link)
    os.remove(link)
    os.rename(filename, link)

    if run:
        run_dotbot(config.file)


def notify(src, dst):
    src = src.replace(HOME, '~')
    dst = dst.replace(HOME, '~')

    if os.path.basename(src) == os.path.basename(dst):
        dst = os.path.dirname(dst)

    LOG.info('Moving {2} from {1} to {0}'.format(dst, *os.path.split(src)))


def run_dotbot(config_file):
    sys.argv[1:] = ['--config-file', config_file]
    dotbot.main()
