import os
import yaml

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

from modbot import DOTFILES
from modbot.config import Config


@pytest.fixture
def config_file():
    data = StringIO()
    data.write('- defaults:\n')
    data.write('    link:\n')
    data.write('      relink: true\n')
    data.write('- clean:\n')
    data.write("  - '~'\n")
    data.write('- link:\n')
    data.write('    ~/.testfile: .testfile]n')
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


def test_config(config, config_contents):
    assert all([a == b for a, b in zip(config.config, config_contents)])


def test_save(config, config_contents, mocker):
    mock_open = mocker.mock_open()
    mock_yaml = mocker.patch('yaml.safe_dump')

    try:
        mock_open = mocker.patch('__builtin__.open', mock_open)
    except ImportError:
        mock_open = mocker.patch('builtins.open', mock_open)

    config.save()

    mock_open.assert_called_once_with(config.file, 'w')
    mock_file = mock_open(config.file, 'w')
    mock_yaml.assert_called_once_with(config_contents, mock_file,
                                      default_flow_style=False)
