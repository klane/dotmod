import os
from collections import namedtuple
from itertools import product

import pytest

from modbot import HOME
from modbot.modbot import remove

DOTFILES = os.path.join(HOME, 'dotfiles')
file = '.testfile'
options = [(None, DOTFILES, 'test'), (file, file + '1')]


@pytest.fixture()
def mocked_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)


@pytest.mark.parametrize('target_path, target', list(product(*options)))
def test_remove(target_path, target, mocker, mocked_modbot):
    config = mocked_modbot.config
    xsource = os.path.join(HOME, file)
    xtarget = os.path.join(target_path or config.path, target)
    config.remove_link.return_value = xsource

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    mocker.patch('os.path.isfile', lambda f: f in (xsource, xtarget))
    mocked_remove = mocker.patch('os.remove')
    remove(config, target)

    config.remove_link.assert_called_once_with(os.path.relpath(xtarget, config.path))
    config.save.assert_called_once()
    mocked_remove.assert_called_once_with(xsource)
    mocked_modbot.rename.assert_called_once_with(xtarget, xsource)
    mocked_modbot.dotbot.assert_called_once_with(config.file)
