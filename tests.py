import pytest
from main import init, add, reset, commit, log, status
from pathlib import Path

init()

def test_init():
    with pytest.raises(SystemExit):
        init()
    assert Path("./.mygit/objects").is_dir()
    assert Path("./.mygit/commits").is_dir()
    assert Path("./.mygit/index.json").exists()
    assert Path("./.mygit/HEAD").exists()
