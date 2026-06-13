from helpers import *

def main():
    # Process the command line arguments using the built in parser
    # Use a match statement to identify the user's action
    # Execute the action
    parser = argparse.ArgumentParser(description="A simple reimplementation of git!")
    parser.add_argument("command", type=str, help="commands include init, add, commit, reset and so on!")
    parser.add_argument("paths", type=str, help="input files", nargs='*')
    args = parser.parse_args()
    execute_command(args.command, args.paths)


def execute_command(command, paths):
    match command:
        
        case "init":
            if valid_init_input(paths):
                init(paths)
            else:
                sys.exit("Invalid Input format; mygit init <one file path>")
    
        case "add":
            if valid_add_input(paths):
                add(paths)
            else:
                sys.exit("Invalid Input format; mygit add <one or more paths>")
            
        case "commit":
            # Call Commit with a message
            ...
        case "log":
            log()
        case "status":
            status()    





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
    

def add(paths):
    # Check whether we have the .mygit directory /
    # Check whether the paths exist /
    # Read the file contents in binary /
    # Compute the hash value according to the file contents /
    # Store the file in the objects directory /
    # (Avoid duplicate objects) /
    # Record the file in index.json ("main.py": "abc...") /
    # If it's already present, update it in the json /

    is_repository_initialized()

    if not files_exist(paths)[0]:
        sys.exit(f"{paths[1]} does not exist.")

    for path in paths:
        with open(path, "rb") as file:
            contents = file.read()
        hash = hashlib.sha256(contents).hexdigest()
        output_path = "./.mygit/objects/" + hash
        if not Path(output_path).exists():
            # Making the new file...
            with open(output_path, "wb") as file:
                file.write(contents)

        # Updating the index
        with open("./.mygit/index.json", "r") as f:
            index = json.load(f)
        
        index[path] = hash

        with open("./.mygit/index.json", "w") as f:
            json.dump(index, f, indent=4)
    


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