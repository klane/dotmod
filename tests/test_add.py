import os
from collections import namedtuple

import pytest

from modbot import HOME
from modbot.modbot import add

DOTFILES = os.path.join(HOME, 'dotfiles')
file = '.testfile'


@pytest.fixture()
def mocked_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)


@pytest.mark.parametrize('source_path, source, target_path, target', [
    (None, file, None, None),
    (None, file, None, file),
    (None, file, None, file + '1'),
    (None, file, DOTFILES, file),
    (None, file, DOTFILES, file + '1'),
    (HOME, file, None, None),
    (HOME, file, None, file),
    (HOME, file, None, file + '1'),
    (HOME, file, DOTFILES, file),
    (HOME, file, DOTFILES, file + '1')
])
def test_add(source_path, source, target_path, target, mocker, mocked_modbot):
    config = mocked_modbot.config
    xsource = os.path.join(source_path or os.getcwd(), source)
    xtarget = os.path.join(target_path or config.path, target or source)
    mocker.patch('os.path.isfile', lambda f: f == xsource)

    if source_path is not None:
        source = os.path.join(source_path, source)

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    add(config, source, target)

    config.add_link.assert_called_once_with(xsource.replace(HOME, '~'), xtarget)
    config.save.assert_called_once()
    mocked_modbot.dotbot.assert_called_once_with(config.file)
    mocked_modbot.rename.assert_called_once_with(xsource, xtarget)
