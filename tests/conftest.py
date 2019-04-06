import os
from collections import namedtuple

import pytest

from modbot import HOME, DOTFILES
from tests import file


@pytest.fixture(autouse=True)
def chdir(monkeypatch):
    monkeypatch.chdir(HOME)


@pytest.fixture
def mock_isfile(mock_modbot, mocker):
    mocker.patch('os.path.isfile', lambda f: f == os.path.join(DOTFILES, file))
    return mock_modbot


@pytest.fixture
def mock_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = os.path.join(config.path, 'install.conf.yaml')

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)
