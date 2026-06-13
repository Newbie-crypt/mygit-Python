from helpers import *

def main():
    # Setting up the Parsers..
    parser = argparse.ArgumentParser(description="A simple reimplementation of git!")
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("files", nargs='*')
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("files", nargs="+")
    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("message", nargs=1)
    checkout_parser = subparsers.add_parser("checkout")
    checkout_parser.add_argument("commit_id", nargs=1)

    args = parser.parse_args()
    execute_command(args)


def execute_command(args):
    match args.command:
        
        case "init":
            if valid_init_input(args.files):
                init(args.files)
            else:
                sys.exit("Invalid Input format; mygit init <one file path>")
    
        case "add":
            if valid_add_input(args.files):
                add(args.files)
            else:
                sys.exit("Invalid Input format; mygit add <one or more paths>")
            
        case "commit":
            commit(args.message)

        case "checkout":
            checkout(args.commit_id)

        case "log":
            log()

        case "status":
            status() 

        case _:
            sys.exit("Unknown command")


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

    is_repository_initialized()

    if not files_exist(paths)[0]:
        sys.exit(f"{paths[1]} does not exist.")

    for path in paths:
        path = path.replace("./","").replace(".\\", "")
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
    

def commit(message):
    is_repository_initialized()
    
    if empty_index():
        sys.exit("No files present in the staging area.")
    
    # Obtaining the commit parent..
    with open(".mygit/HEAD", 'r') as f:
        commit_parent = f.read()

    # Setting up the files to be committed..
    with open("./.mygit/index.json", "r") as f:
        files = json.load(f)

    if commit_parent != "null":
        with open(f"./.mygit/commits/{commit_parent}.json", "r") as f:
            commit_parent_json = json.load(f)

        for key in commit_parent_json["files"]:
            if key not in files:
                files[key] = commit_parent_json["files"][key]

    # Setting up the data to be stored in the commit json file
    commit_data = {
        "parent_commit": commit_parent,
        "message": message,
        "timestamp": datetime.datetime.now().timestamp(),
        "files": files
    }

    commit_id = hashlib.sha256(json.dumps(commit_data).encode("utf-8")).hexdigest()

    # Creating the json file..
    with open(f".mygit/commits/{commit_id}.json", 'w') as f:
        json.dump(commit_data, f, indent=4)

    # Update HEAD
    with open(".mygit/HEAD", 'w') as f:
        f.write(commit_id)
    
    # Clearing the staging area (index.json)
    with open(".mygit/index.json", 'w') as f:
        f.write("{}")

    # Returned for unit testing purposes
    return commit_id, files
    
    

def checkout(commit_id):
    # Check whether repo is initialized /
    # Check whether commit id exists (check the commit files in /commits) /
    # Restore the files in the snapshot (by creating or overwriting) /
        # loop through the files dict in the commit
        # read the contents of one key (in binary)
        # write the contents to the file which has the name of the key
    # Delete files that are not present in the snapshot /
    # NEVER DELETE .mygit /
    # Update HEAD /
    # clear staging area /
    is_repository_initialized()

    # Ensuring the commit id exists..
    path = f".mygit/commits/{commit_id}.json"
    if not Path(path).exists():
        sys.exit("Invalid Commit ID")

    # Creating/Overwriting files..
    with open(path, 'r') as f:
        contents = json.load(f)
    files = contents["files"]
    for key in files:
        with open(f".mygit/objects/{files[key]}", "rb") as f:
            input_data = f.read()
        with open(key, "wb") as f:
            f.write(input_data)
    
    # Removing files/directories not present in the snapshot...
    current_directory_files = list(Path(".").glob("*"))
    for file in current_directory_files:
        if file not in files and ".mygit" not in str(file):
            if file.is_file():
                file.unlink()          # remove file
            elif file.is_dir():
                shutil.rmtree(file)  
    
    # Changing the HEAD..
    with open(".mygit/HEAD", 'w') as f:
        f.write(commit_id)
    
    # Clearing the staging area (index.json)
    with open(".mygit/index.json", 'w') as f:
        f.write("{}")
    





def log():
    ...

def status():
    ...

if __name__ == "__main__":
    main()