import argparse

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
    ...

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