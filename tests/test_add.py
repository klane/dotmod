import os
from collections import namedtuple

import pytest

from modbot import HOME
from modbot.modbot import add

DOTFILES = os.path.join(HOME, 'dotfiles')
filename = '.testfile'


@pytest.fixture()
def mocked_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)


@pytest.mark.parametrize('source_path, source_file, target_path, target_file', [
    (None, filename, None, None),
    (None, filename, None, filename),
    (None, filename, None, filename + '1'),
    (None, filename, DOTFILES, filename),
    (None, filename, DOTFILES, filename + '1'),
    (HOME, filename, None, None),
    (HOME, filename, None, filename),
    (HOME, filename, None, filename + '1'),
    (HOME, filename, DOTFILES, filename),
    (HOME, filename, DOTFILES, filename + '1')
])
def test_add(source_path, source_file, target_path, target_file, mocker, mocked_modbot):
    config = mocked_modbot.config

    if source_path is None:
        source_path = os.getcwd()
        source = source_file
    else:
        source = os.path.join(source_path, source_file)

    if target_path is None:
        target_path = config.path
        target = target_file
    else:
        target = os.path.join(target_path, target_file)

    xsource = os.path.join(source_path, source_file)

    if target_file is None:
        xtarget = os.path.join(target_path, source_file)
    else:
        xtarget = os.path.join(target_path, target_file)

    mocker.patch('os.path.isfile', lambda file: file == xsource)

    if target is None:
        add(config, source)
    else:
        add(config, source, target)

    config.add_link.assert_called_once_with(xsource.replace(HOME, '~'), xtarget)
    config.save.assert_called_once()
    mocked_modbot.dotbot.assert_called_once_with(config.file)
    mocked_modbot.rename.assert_called_once_with(xsource, xtarget)
