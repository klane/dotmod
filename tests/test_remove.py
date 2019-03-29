from itertools import product

from modbot.modbot import remove
from tests import *

options = [(None, DOTFILES, 'test'), (file, file + '1')]
options = list(product(*options))


@pytest.fixture
def mocked_isfile(mocked_modbot, mocker):
    mocker.patch('os.path.isfile', lambda f: f == os.path.join(DOTFILES, file))
    return mocked_modbot


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
    mocked_remove.assert_called_once_with(xsource)
    mocked_modbot.rename.assert_called_once_with(xtarget, xsource)
    mocked_modbot.dotbot.assert_called_once_with(config.file)

    try:
        config.save.assert_called_once()
    except AttributeError:
        pass


@pytest.mark.parametrize('mocks, message', [
    (pytest.lazy_fixture('mocked_modbot'), 'not in repo'),
    (pytest.lazy_fixture('mocked_isfile'), 'does not exist')
])
def test_exceptions(mocks, message):
    with pytest.raises(OSError, match=message):
        remove(mocks.config, file)
