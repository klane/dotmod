import os
from collections import namedtuple

import pytest

from modbot import HOME
from modbot.modbot import add

filename = '.testfile'
source = os.path.join(HOME, filename)
target = os.path.join(os.getcwd(), filename)


@pytest.fixture()
def modbot_mock(mocker):
    config = mocker.MagicMock()
    config.path = os.path.join(HOME, 'project', 'modbot')
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')
    mocker.patch('os.path.isfile', lambda file: file == source)

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)


def test_add(modbot_mock):
    config = modbot_mock.config
    add(config, source)

    config.add_link.assert_called_once_with(source.replace(HOME, '~'), target)
    config.save.assert_called_once()
    modbot_mock.dotbot.assert_called_once_with(config.file)
    modbot_mock.rename.assert_called_once_with(source, target)
