import os
import sys

import pytest

from modbot import DOTFILES
from tests import CONFIG_FILE, FILE


def test_config(mock_config, config_contents):
    config = mock_config.config
    i = [i for (i, x) in enumerate(config_contents) if 'link' in x.keys()][0]
    assert config.path == DOTFILES
    assert config.file == CONFIG_FILE
    assert all(a == b for a, b in zip(config.contents, config_contents))
    assert all(a == b for a, b in zip(config.links, config_contents[i]['link']))


def test_add_link(mock_config):
    config = mock_config.config
    n = len(config.links)
    newfile = FILE + '1'
    config.add_link('~/' + newfile, os.path.join(DOTFILES, newfile))
    assert len(config.links) == n + 1
    assert config.links['~/' + newfile] == newfile


def test_remove_link(mock_config):
    config = mock_config.config
    n = len(config.links)
    key = config.remove_link(FILE)
    assert len(config.links) == n - 1
    assert key == '~/' + FILE


@pytest.mark.skipif(sys.version_info.major == 2, reason='requires python3')
def test_save(mock_config, config_contents, mocker):
    config = mock_config.config
    mock_open = mocker.mock_open()
    mock_yaml = mocker.patch('yaml.safe_dump')
    mocker.patch('builtins.open', mock_open)

    config.save()

    mock_open.assert_called_once_with(config.file, 'w')
    mock_file = mock_open(config.file, 'w')
    mock_yaml.assert_called_once_with(
        config_contents, mock_file, default_flow_style=False
    )


def test_open(mock_config):
    mock_config.open.assert_called_once_with(mock_config.config.file)
