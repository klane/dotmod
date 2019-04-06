import os
from collections import namedtuple

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest
import yaml

from modbot import HOME, DOTFILES
from modbot.config import Config
from tests import file


@pytest.fixture(autouse=True)
def chdir(monkeypatch):
    monkeypatch.chdir(HOME)


@pytest.fixture
def config_file():
    data = StringIO()
    data.write('- defaults:\n')
    data.write('    link:\n')
    data.write('      relink: true\n')
    data.write('- clean:\n')
    data.write("  - '~'\n")
    data.write('- link:\n')
    data.write('    ~/.testfile: .testfile\n')
    return data.getvalue()


@pytest.fixture
def config_contents(config_file):
    return yaml.safe_load(config_file)


@pytest.fixture(params=[
    'install.conf.yaml',
    os.path.join(DOTFILES, 'install.conf.yaml')
])
def config(config_file, mocker, request):
    mock_open = mocker.mock_open(read_data=config_file)

    try:
        mocker.patch('__builtin__.open', mock_open)
    except ImportError:
        mocker.patch('builtins.open', mock_open)

    return Config(request.param)


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
