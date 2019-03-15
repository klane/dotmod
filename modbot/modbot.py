import os
import sys
import dotbot
from modbot import HOME, LOG
from modbot.config import Config


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
