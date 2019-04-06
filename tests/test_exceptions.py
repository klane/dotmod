import os

import pytest

from modbot import DOTFILES
from modbot.modbot import add, remove
from tests import file


@pytest.mark.parametrize('function, mocks, message', [
    (add, pytest.lazy_fixture('mock_modbot'), 'does not exist'),
    (add, pytest.lazy_fixture('mock_isfile'), 'already linked'),
    (remove, pytest.lazy_fixture('mock_modbot'), 'not in repo'),
    (remove, pytest.lazy_fixture('mock_isfile'), 'does not exist')
])
def test_modbot_exceptions(function, mocks, message):
    with pytest.raises(OSError, match=message):
        function(mocks.config, os.path.join(DOTFILES, file))
