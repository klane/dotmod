from itertools import product

from modbot.modbot import remove
from tests import *

options = [(None, DOTFILES, 'test'), (file, file + '1')]
options = list(product(*options))


@pytest.mark.parametrize('target_path, target', options)
def test_remove(target_path, target, mocked_modbot, mocker):
    config = mocked_modbot.config
    xsource = os.path.join(HOME, file)
    xtarget = os.path.join(target_path or config.path, target)
    config.remove_link.return_value = xsource

    if target_path is not None:
        target = os.path.join(target_path, target)

    if config.path not in xtarget:
        xtarget = os.path.join(config.path, xtarget)

    mocker.patch('os.path.isfile', lambda f: f in (xsource, xtarget))
    mocked_remove = mocker.patch('os.remove')
    remove(config, target)

    config.remove_link.assert_called_once_with(os.path.relpath(xtarget, config.path))
    config.save.assert_called_once()
    mocked_remove.assert_called_once_with(xsource)
    mocked_modbot.rename.assert_called_once_with(xtarget, xsource)
    mocked_modbot.dotbot.assert_called_once_with(config.file)
