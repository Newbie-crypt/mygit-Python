import argparse
import os
from pathlib import Path
import sys
import hashlib
import json


# we want to make sure of the following:
# only one directory path is inputted
def valid_init_input(paths):
    return len(paths) == 1 or len(paths) == 0


def valid_add_input(paths):
    return not len(paths) == 0


def files_exist(paths):
    for path in paths:
        if not Path(path).exists():
            return (False, path)
    return (True, "null")
        
def is_repository_initialized():
    if not Path("./.mygit").exists():
        sys.exit("Repository not initialized")
    return True

def empty_index():
    with open("./.mygit/index.json", "r") as f:
        index = json.load(f)
    return not index