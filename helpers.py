import argparse
import os
from pathlib import Path
import sys


# we want to make sure of the following:
# only one directory path is inputted
def valid_init_input(paths):
    return len(paths) == 1 or len(paths) == 0


def valid_add_input(paths):
    return not len(paths) == 0


def files_exist(paths):
    ...