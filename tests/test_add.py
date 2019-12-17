import os

import pytest

from modbot import DOTFILES, HOME
from modbot.modbot import add
from tests import file


@pytest.mark.parametrize('source_path', (None, HOME))
@pytest.mark.parametrize('source', [file])
@pytest.mark.parametrize('target_path', (None, DOTFILES, 'test'))
@pytest.mark.parametrize('target', (None, file, file + '1'))
@pytest.mark.parametrize('run', (False, True))
def test_add(source_path, source, target_path, target, run, mock_modbot, mocker):
    config = mock_modbot.config
    xsource = os.path.join(source_path or os.getcwd(), source)
    xtarget = os.path.join(target_path or config.path, target or source)
    mocker.patch('os.path.isfile', lambda f: f == xsource)

    if source_path is not None:
        source = os.path.join(source_path, source)

    if target_path is not None:
        target = os.path.join(target_path, target or '')

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    add(config, source, target, run)

    config.add_link.assert_called_once_with(xsource.replace(HOME, '~'), xtarget)
    config.save.assert_called_once_with()
    mock_modbot.rename.assert_called_once_with(xsource, xtarget)

    if run:
        mock_modbot.dotbot.assert_called_once_with(config.file)
    else:
        mock_modbot.dotbot.assert_not_called()
