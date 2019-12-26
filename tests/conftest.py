import os
from collections import namedtuple

import pytest
import yaml

from modbot import DOTFILES, HOME
from modbot.config import Config
from tests import config_file, file, repo_file

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@pytest.fixture(autouse=True)
def chdir(monkeypatch):
    monkeypatch.chdir(HOME)


@pytest.fixture
def config_yaml():
    data = StringIO()
    data.write('- defaults:\n')
    data.write('    link:\n')
    data.write('      relink: true\n')
    data.write('- clean:\n')
    data.write("  - '~'\n")
    data.write('- link:\n')
    data.write('    ~/{0}: {0}\n'.format(file))
    return data.getvalue()


@pytest.fixture
def config_contents(config_yaml):
    return yaml.safe_load(config_yaml)


@pytest.fixture(params=[os.path.basename(config_file), config_file])
def mock_config(config_yaml, mocker, request):
    mock_open = mocker.mock_open(read_data=config_yaml)

    try:
        mocker.patch('__builtin__.open', mock_open)
    except ImportError:
        mocker.patch('builtins.open', mock_open)

    config = Config(request.param)
    mocks = namedtuple('mocks', 'config open')
    return mocks(config, mock_open)


@pytest.fixture
def mock_isfile(mock_modbot, mocker):
    mocker.patch('os.path.isfile', lambda filename: filename == repo_file)
    return mock_modbot


@pytest.fixture
def mock_modbot(mocker):
    config = mocker.MagicMock()
    config.path = DOTFILES
    config.file = config_file

    dotbot = mocker.patch('modbot.modbot.run_dotbot')
    rename = mocker.patch('os.rename')

    mocks = namedtuple('mocks', 'config dotbot rename')
    return mocks(config, dotbot, rename)
