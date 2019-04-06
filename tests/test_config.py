def test_config(config, config_contents):
    assert all([a == b for a, b in zip(config.config, config_contents)])


def test_save(config, config_contents, mocker):
    mock_open = mocker.mock_open()
    mock_yaml = mocker.patch('yaml.safe_dump')

    try:
        mock_open = mocker.patch('__builtin__.open', mock_open)
    except ImportError:
        mock_open = mocker.patch('builtins.open', mock_open)

    config.save()

    mock_open.assert_called_once_with(config.file, 'w')
    mock_file = mock_open(config.file, 'w')
    mock_yaml.assert_called_once_with(config_contents, mock_file,
                                      default_flow_style=False)
