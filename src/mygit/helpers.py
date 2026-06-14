import argparse
from pathlib import Path
import sys
import hashlib
import json
import datetime
import shutil


# we want to make sure of the following:
# only one directory path is inputted
def valid_init_input(paths):
    return len(paths) == 1 or len(paths) == 0


def valid_add_input(paths):
    return not len(paths) == 0


def files_exist(paths, repo_directory="."):
    for path in paths:
        if not Path(f"{repo_directory}/{path}").exists():
            return (False, path)
    return (True, "null")


def is_repository_initialized(repo_directory="."):
    if not Path(f"{repo_directory}/.mygit").exists():
        sys.exit("Repository not initialized")
    return True


def empty_index(repo_directory="."):
    with open(f"{repo_directory}/.mygit/index.json", "r") as f:
        index = json.load(f)
    return not index


def get_HEAD_id(repo_directory):
    with open(f"{repo_directory}/.mygit/HEAD", "r") as f:
        current_commit_id = f.read()
    return current_commit_id


def get_staged_files(repo_directory):
    with open(f"{repo_directory}/.mygit/index.json", "r") as f:
        contents = json.load(f)
    return [key for key in contents]


# Detect modified files; a file is modified if it's in the HEAD commit, exists in the working directory, its current hash != hash in HEAd,
# not staged
def get_modified_files(repo_directory):
    current_commit_id = get_HEAD_id(repo_directory)
    if current_commit_id == "null":
        return []

    with open(f"{repo_directory}/.mygit/commits/{current_commit_id}.json", "r") as f:
        commit_files = (json.load(f))["files"]

    modified = []

    # Looping through the files in working directory
    current_directory_files = list(Path(repo_directory).glob("*"))
    for file in current_directory_files:
        filename = str(file).split("\\")[-1]
        if filename == ".mygit":
            continue

        if filename not in commit_files:
            continue

        with open(str(file), "rb") as f:
            contents = f.read()
        hash = hashlib.sha256(contents).hexdigest()

        if hash == commit_files[filename]:
            continue

        with open(f"{repo_directory}/.mygit/index.json", "r") as f:
            contents = json.load(f)
        if filename in contents:
            continue

        modified.append(filename)

    return modified


def get_untracked_files(repo_directory):

    current_directory_files = list(Path(repo_directory).glob("*"))
    current_commit_id = get_HEAD_id(repo_directory)
    if current_commit_id == "null":
        return [
            str(file).split("\\")[-1]
            for file in current_directory_files
            if str(file).split("\\")[-1] != ".mygit"
        ]

    untracked = []

    with open(f"{repo_directory}/.mygit/commits/{current_commit_id}.json", "r") as f:
        commit_files = (json.load(f))["files"]

    # Looping through the files in working directory
    for file in current_directory_files:
        filename = str(file).split("\\")[-1]
        if filename == ".mygit" or filename in commit_files:
            continue

        with open(f"{repo_directory}/.mygit/index.json", "r") as f:
            contents = json.load(f)
        if filename in contents:
            continue

        untracked.append(filename)

    return untracked
