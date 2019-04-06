import os

import pytest

from modbot import DOTFILES
from modbot.modbot import add, remove
from modbot.config import Config, ConfigError
from tests import file, repo_file


@pytest.mark.parametrize('function, mocks, message', [
    (add, pytest.lazy_fixture('mock_modbot'), 'does not exist'),
    (add, pytest.lazy_fixture('mock_isfile'), 'already linked'),
    (remove, pytest.lazy_fixture('mock_modbot'), 'not in repo'),
    (remove, pytest.lazy_fixture('mock_isfile'), 'does not exist')
])
def test_modbot_exceptions(function, mocks, message):
    with pytest.raises(OSError, match=message):
        function(mocks.config, repo_file)


@pytest.mark.parametrize('method, inputs, message', [
    (Config.add_link, ['~/' + file, repo_file], 'already in config'),
    (Config.remove_link, [os.path.join(DOTFILES, '.fakefile')], 'not in config')
])
def test_config_exceptions(mock_config, method, inputs, message):
    config = mock_config.config

    with pytest.raises(ConfigError, match=message):
        method(config, *inputs)
