import os
from itertools import product

import pytest

from modbot import HOME, DOTFILES
from modbot.modbot import remove
from tests import file

options = [(None, DOTFILES, 'test'), (file, file + '1')]
options = list(product(*options))


@pytest.mark.parametrize('target_path, target', options)
def test_remove(target_path, target, mock_modbot, mocker):
    config = mock_modbot.config
    xsource = os.path.join(HOME, file)
    xtarget = os.path.join(target_path or config.path, target)
    config.remove_link.return_value = xsource

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    mocker.patch('os.path.isfile', lambda f: f in (xsource, xtarget))
    mock_remove = mocker.patch('os.remove')
    remove(config, target)

    config.remove_link.assert_called_once_with(os.path.relpath(xtarget, config.path))
    config.save.assert_called_once_with()
    mock_remove.assert_called_once_with(xsource)
    mock_modbot.rename.assert_called_once_with(xtarget, xsource)
    mock_modbot.dotbot.assert_called_once_with(config.file)
