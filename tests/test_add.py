from itertools import product

from modbot.modbot import add
from tests import *

options = [(None, HOME), [file], (None, DOTFILES, 'test'), (None, file, file + '1')]
options = [o for o in product(*options) if o[2] is None or o[3] is not None]


@pytest.fixture
def mocked_isfile(mocked_modbot, mocker):
    mocker.patch('os.path.isfile')
    return mocked_modbot


@pytest.mark.parametrize('source_path, source, target_path, target', options)
def test_add(source_path, source, target_path, target, mocked_modbot, mocker):
    config = mocked_modbot.config
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
    mocked_modbot.rename.assert_called_once_with(xsource, xtarget)
    mocked_modbot.dotbot.assert_called_once_with(config.file)


@pytest.mark.parametrize('mocks, message', [
    (pytest.lazy_fixture('mocked_modbot'), 'does not exist'),
    (pytest.lazy_fixture('mocked_isfile'), 'already linked')
])
def test_exceptions(mocks, message):
    with pytest.raises(OSError, match=message):
        add(mocks.config, file)
