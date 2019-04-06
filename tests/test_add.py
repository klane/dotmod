import os
from itertools import product

import pytest

from modbot import HOME, DOTFILES
from modbot.modbot import add
from tests import file

options = [(None, HOME), [file], (None, DOTFILES, 'test'), (None, file, file + '1')]
options = [o for o in product(*options) if o[2] is None or o[3] is not None]


@pytest.mark.parametrize('source_path, source, target_path, target', options)
def test_add(source_path, source, target_path, target, mock_modbot, mocker):
    config = mock_modbot.config
    xsource = os.path.join(source_path or os.getcwd(), source)
    xtarget = os.path.join(target_path or config.path, target or source)
    mocker.patch('os.path.isfile', lambda f: f == xsource)

    if source_path is not None:
        source = os.path.join(source_path, source)

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    add(config, source, target)

    config.add_link.assert_called_once_with(xsource.replace(HOME, '~'), xtarget)
    config.save.assert_called_once_with()
    mock_modbot.rename.assert_called_once_with(xsource, xtarget)
    mock_modbot.dotbot.assert_called_once_with(config.file)
