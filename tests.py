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
    assert files_exist(["main.py", "helpers.py"]) == (True, "null")
    assert files_exist(["foo", "bar"]) == (False, "foo")

def test_correct_use_of_add():
    init([])
    add(["main.py"])
    with open("main.py", "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    output_path = "./.mygit/objects/" + hash
    assert Path(output_path).exists() == True

    with open("./.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {"main.py": hash}
    shutil.rmtree(".mygit")

def test_correct_use_of_add_after_updating_staged_file():
    init([])
    path = "./test.txt"
    file = Path(path)
    file.touch()
    file.write_text("Hello World\n")
    add([path])

    file.write_text("Hello again.\n")
    add([path])
    with open(path, "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    output_path = "./.mygit/objects/" + hash
    assert Path(output_path).exists() == True

    with open("./.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {path: hash}

    # Removing files and .mygit
    file.unlink()
    shutil.rmtree(".mygit")

def test_add_no_duplicates():
    init([])
    path = "./test.txt"
    file = Path(path)
    file.touch()
    file.write_text("Hello World\n")
    with open(path, "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    add([path])
    add([path])
    with open("./.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {path: hash}

    # Removing files and .mygit
    file.unlink()
    shutil.rmtree(".mygit")

def test_empty_index():
    init([])
    assert empty_index() == True
    path = "./test.txt"
    file = Path(path)
    file.touch()
    file.write_text("Hello World\n")
    add([path])
    assert empty_index() == False

    # Removing files and .mygit
    file.unlink()
    shutil.rmtree(".mygit")

def test_commit_with_no_staged_files():
    ...

def test_commit_with_staged_files_with_null_parent_commit():
    ...

def test_commit_with_staged_files_with_parent_commit():
    ...
    

    

    

