import argparse
import os
from pathlib import Path
import sys
import hashlib
import json
import uuid
import datetime
import shutil


# we want to make sure of the following:
# only one directory path is inputted
def valid_init_input(paths):
    return len(paths) == 1 or len(paths) == 0


def valid_add_input(paths):
    return not len(paths) == 0


def files_exist(paths, repo_directory='.'):
    for path in paths:
        if not Path(f"{repo_directory}/{path}").exists():
            return (False, path)
    return (True, "null")
        
def is_repository_initialized(repo_directory='.'):
    if not Path(f"{repo_directory}/.mygit").exists():
        sys.exit("Repository not initialized")
    return True

def empty_index():
    with open("./.mygit/index.json", "r") as f:
        index = json.load(f)
    return not index

