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
    parser.add_argument("paths", type=str, help="input files", nargs='*')
    args = parser.parse_args()
    print(args.paths)
    execute_command(args.command, args.paths)


def execute_command(command, paths):
    match command:
        
        case "init":
            if valid_init_input(paths):
                init(paths)
            else:
                sys.exit("Invalid Input format; mygit init <one file path>")
    
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



# we want to make sure of the following:
# only one directory path is inputted
def valid_init_input(paths):
    return len(paths) == 1 or len(paths) == 0


def init(paths):

    # If no path is provided, then add the .mygit to the current directory
    if not paths:
        directory = '.'
    else:
        directory = paths[0]
    
    if not Path(directory).exists():
        Path(directory).mkdir()

    try:
        Path(f"{directory}/.mygit").mkdir()
    except FileExistsError:
        sys.exit("Repository already initialized")
    else:
        Path(f"{directory}/.mygit/objects").mkdir()
        Path(f"{directory}/.mygit/commits").mkdir()
        Path(f"{directory}/.mygit/index.json").touch()
        Path(f"{directory}/.mygit/index.json").write_text("{}")
        Path(f"{directory}/.mygit/HEAD").touch()
        Path(f"{directory}/.mygit/HEAD").write_bytes(b"null")
    

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