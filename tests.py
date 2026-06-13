import pytest
from mygit.repository import *
from mygit.helpers import *

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

def test_init_another_directory(tmp_path):
    init([tmp_path])
    with pytest.raises(SystemExit):
        init([tmp_path])
    assert Path(f"{tmp_path}/.mygit/objects").is_dir()
    assert Path(f"{tmp_path}/.mygit/commits").is_dir()
    assert Path(f"{tmp_path}/.mygit/index.json").exists()
    assert Path(f"{tmp_path}/.mygit/HEAD").exists()
    shutil.rmtree(tmp_path)

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
    assert files_exist(["tests.py"]) == (True, "null")
    assert files_exist(["foo", "bar"]) == (False, "foo")

def test_correct_use_of_add(tmp_path):
    init([str(tmp_path)])
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    p.write_text("hello")
    add([filename], repo_directory=str(tmp_path))
    with open(str(p), "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    output_path = f"{str(tmp_path)}/.mygit/objects/" + hash
    assert Path(output_path).exists() == True

    with open(f"{str(tmp_path)}/.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {filename: hash}

def test_correct_use_of_add_after_updating_staged_file(tmp_path):
    init([str(tmp_path)])
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    p.write_text("hello")
    add([filename], repo_directory=str(tmp_path))

    p.write_text("Hello again.\n")
    add([filename], repo_directory=str(tmp_path))
    with open(str(p), "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    output_path = f"{str(tmp_path)}/.mygit/objects/" + hash
    assert Path(output_path).exists() == True

    with open(f"{str(tmp_path)}/.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {filename: hash}


def test_add_no_duplicates(tmp_path):
    init([str(tmp_path)])
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    p.write_text("hello")
    path = str(p)
    with open(p, "rb") as f:
        contents = f.read()
    hash = hashlib.sha256(contents).hexdigest()
    add([filename], repo_directory=str(tmp_path))
    add([filename], repo_directory=str(tmp_path))
    with open(f"{str(tmp_path)}/.mygit/index.json", "r") as f:
        index = json.load(f)
    assert index == {filename: hash}


def test_empty_index(tmp_path):
    init([str(tmp_path)])
    assert empty_index(str(tmp_path)) == True
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    p.write_text("hello")
    path = str(p)
    add([filename], repo_directory=str(tmp_path))
    assert empty_index(str(tmp_path)) == False

def test_commit_with_no_staged_files(tmp_path):
    init([str(tmp_path)])
    with pytest.raises(SystemExit):
        commit("foo")

def test_commit_with_staged_files_with_null_parent_commit(tmp_path):
    init([str(tmp_path)])
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    p.write_text("hello")
    path = str(p)
    add([filename], repo_directory=str(tmp_path))
    commit_message = "test commit"
    commit_id, files = commit(commit_message, repo_directory=str(tmp_path))

    # Ensuring that the commit json is correct
    commit_files = list(Path(f"{str(tmp_path)}/.mygit/commits").glob("*.json"))
    assert len(commit_files) == 1
    with open(str(commit_files[0]), 'r') as f:
        contents = json.load(f)
    assert contents["parent_commit"] == "null"
    assert contents["message"] == commit_message
    assert contents["files"] == files
    
    # Ensuring that the HEAD pointer is updated
    with open(f"{str(tmp_path)}/.mygit/HEAD", 'r') as f:
        id = f.read()
    assert id == commit_id

    # Ensuring that the staging area is cleared
    with open(f"{str(tmp_path)}/.mygit/index.json", 'r') as f:
        contents = json.load(f)
    assert not contents

def test_commit_with_staged_files_with_parent_commit(tmp_path):
    init([str(tmp_path)])
    filename = "hello.txt"
    p = tmp_path / filename
    p.touch()
    path = str(p)

    # First commit
    p.write_text("Hello World\n")
    add([path])
    first_commit_id, first_files = commit("first commit")

    # Second Commit
    file.write_text("Hello, again\n")
    add([path])
    second_commit_id, second_files = commit("second commit")

    # Ensuring that there are two commit files..
    commit_files = list(Path(".mygit/commits").glob("*.json"))
    assert len(commit_files) == 2

    for file in commit_files:
        if second_commit_id in str(file):
            with open(str(file), 'r') as f:
                contents = json.load(f)
            assert contents["parent_commit"] == first_commit_id
            assert contents["message"] == "second commit"
            assert contents["files"] == second_files

    
# def test_checkout_invalid_commitID():
#     ...

# def test_checkout_valid_commitID():
#     ...
    

    

