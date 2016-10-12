import os
import pytest
from lib.utils import which, BadKarma, tower_cli_executable


CURRENT_FILE = __file__
CURRENT_DIR = os.path.abspath(os.path.dirname(CURRENT_FILE))


def test_which(monkeypatch):
    fake_path = ':'.join(('/bin', CURRENT_DIR))
    monkeypatch.setitem(os.environ, 'PATH', fake_path)
    assert os.path.abspath(CURRENT_FILE) == which(CURRENT_FILE)
    with pytest.raises(BadKarma):
        which('non-existing-executable')


def test_tower_cli_executable(monkeypatch):
    # monkeypatch.setitem(os.environ, 'PATH', fake_path)
    def mockreturn(path):
        return True
    monkeypatch.setattr(os.path, 'isfile', mockreturn)
    assert tower_cli_executable() != ''
