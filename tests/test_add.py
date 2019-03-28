import os
from collections import namedtuple

import pytest

from modbot import HOME
from modbot.modbot import add

DOTFILES = os.path.join(HOME, 'dotfiles')
filename = '.testfile'
source = os.path.join(HOME, filename)
target = os.path.join(DOTFILES, filename)


@pytest.fixture()
def mocked_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')
    mocker.patch('os.path.isfile', lambda file: file == source)

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)


def test_add(mocked_modbot):
    config = mocked_modbot.config
    add(config, source)

    config.add_link.assert_called_once_with(source.replace(HOME, '~'), target)
    config.save.assert_called_once()
    mocked_modbot.dotbot.assert_called_once_with(config.file)
    mocked_modbot.rename.assert_called_once_with(source, target)
