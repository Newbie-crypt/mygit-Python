import pytest
from main import *
from helpers import *
from pathlib import Path
import shutil

def test_execute_command():
    ...

def test_valid_init_inputs():
    assert valid_init_input(["lol"]) == True
    assert valid_init_input(["foo", "bar"]) == False

def test_init_current_directory():
    init([])
    with pytest.raises(SystemExit):
        init([])
    assert Path("./.mygit/objects").is_dir()
    assert Path("./.mygit/commits").is_dir()
    assert Path("./.mygit/index.json").exists()
    assert Path("./.mygit/HEAD").exists()
    shutil.rmtree(".mygit")

def test_init_another_directory():
    directory = "foo"
    init([directory])
    with pytest.raises(SystemExit):
        init([directory])
    assert Path(f"{directory}/.mygit/objects").is_dir()
    assert Path(f"{directory}/.mygit/commits").is_dir()
    assert Path(f"{directory}/.mygit/index.json").exists()
    assert Path(f"{directory}/.mygit/HEAD").exists()
    shutil.rmtree(directory)

def test_valid_add_input():
    assert valid_add_input([]) == False
    assert valid_add_input(["foo"]) == True
    assert valid_add_input(["foo", "bar"]) == True

def test_is_repository_initialized():
    init([])
    assert is_repository_initialized() == True
    shutil.rmtree(".mygit")
    with pytest.raises(SystemExit):
        is_repository_initialized()

def test_files_exist():
    assert files_exist(["main.py", "helpers.py"]) == True
    assert files_exist(["foo", "bar"]) == (False, "foo")
    

    

