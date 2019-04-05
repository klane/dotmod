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


@pytest.fixture(params=[
    'install.conf.yaml',
    os.path.join(DOTFILES, 'install.conf.yaml')
])
def config(config_file, mocker, request):
    mock_open = mocker.mock_open(read_data=config_file)

    try:
        mocker.patch('__builtin__.open', mock_open)
    except ModuleNotFoundError:
        mocker.patch('builtins.open', mock_open)

    return Config(request.param)


def test_config(config, config_file):
    assert all([a == b for a, b in zip(config.config, yaml.safe_load(config_file))])
