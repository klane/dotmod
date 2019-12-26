import os

import pytest

from modbot import DOTFILES, HOME
from modbot.modbot import remove
from tests import FILE


@pytest.mark.parametrize('target_path', (None, DOTFILES, 'test'))
@pytest.mark.parametrize('target', (FILE, FILE + '1'))
@pytest.mark.parametrize('run', (False, True))
def test_remove(target_path, target, run, mock_modbot, mocker):
    config = mock_modbot.config
    xsource = os.path.join(HOME, FILE)
    xtarget = os.path.join(target_path or config.path, target)
    config.remove_link.return_value = xsource

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    mocker.patch('os.path.isfile', lambda filename: filename in (xsource, xtarget))
    mock_remove = mocker.patch('os.remove')
    remove(config, target, run)

    config.remove_link.assert_called_once_with(os.path.relpath(xtarget, config.path))
    config.save.assert_called_once_with()
    mock_remove.assert_called_once_with(xsource)
    mock_modbot.rename.assert_called_once_with(xtarget, xsource)

    if run:
        mock_modbot.dotbot.assert_called_once_with()
    else:
        mock_modbot.dotbot.assert_not_called()
