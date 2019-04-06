import os

from modbot import DOTFILES
from tests import config_file


def test_config(mock_config, config_contents):
    i = [i for (i, x) in enumerate(config_contents) if 'link' in x.keys()][0]
    assert mock_config.path == DOTFILES
    assert mock_config.file == os.path.join(DOTFILES, config_file)
    assert all([a == b for a, b in zip(mock_config.config, config_contents)])
    assert all([a == b for a, b in zip(mock_config.links, config_contents[i]['link'])])


def test_save(mock_config, config_contents, mocker):
    mock_open = mocker.mock_open()
    mock_yaml = mocker.patch('yaml.safe_dump')

    try:
        mock_open = mocker.patch('__builtin__.open', mock_open)
    except ImportError:
        mock_open = mocker.patch('builtins.open', mock_open)

    mock_config.save()

    mock_open.assert_called_once_with(mock_config.file, 'w')
    mock_file = mock_open(mock_config.file, 'w')
    mock_yaml.assert_called_once_with(config_contents, mock_file,
                                      default_flow_style=False)
