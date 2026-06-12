import argparse
import os
from pathlib import Path
import sys

def main():
    # Process the command line arguments using the built in parser
    # Use a match statement to identify the user's action
    # Execute the action
    parser = argparse.ArgumentParser(description="A simple reimplementation of git!")
    parser.add_argument("command", type=str, help="commands include init, add, commit, reset and so on!")
    args = parser.parse_args()
    match args.command:
        case "init":
            init()
        case "add":
            # Figure out how to identify the file_path and/or filenames
            ...
        case "reset":
            # (the reverse of add)
            ...
        case "commit":
            # Call Commit with a message
            ...
        case "log":
            log()
        case "status":
            status()



def init():
    try:
        Path("./.mygit").mkdir()
    except FileExistsError:
        sys.exit("Repository already initialized")
    else:
        Path("./.mygit/objects").mkdir()
        Path("./.mygit/commits").mkdir()
        Path("./.mygit/index.json").touch()
        Path("./.mygit/index.json").write_text("{}")
        Path("./.mygit/HEAD").touch()
        Path("./.mygit/HEAD").write_bytes(b"null")


def add(file_path):
    ...

def reset():
    ...

def commit(message):
    ...

def log():
    ...

def status():
    ...

if __name__ == "__main__":
    main()