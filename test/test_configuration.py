import os
import pytest
from lib.utils import BadKarma
from lib.configuration import Config

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def test_configuration_initialization():
    config_file = os.path.join(CURRENT_DIR, 'empty_config_1')
    config = Config(config_file)
    assert config.configparser.has_section('general') == True
    with pytest.raises(BadKarma):
        config.get('this value does not exist')


def test_values_from_environment():
    config_file = os.path.join(CURRENT_DIR, 'empty_config_1')
    config = Config(config_file)
    path = os.environ['PATH']
    config._update_from_env('PATH', 'path')
    assert config.has_option('path') == True
    assert config.get('path') == path
