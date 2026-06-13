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
    # Check whether repo is initialized /
    # Check whether the staging area (index.json) is not empty /
    # read current HEAD /
    # create a <commit id>.json file (id is generated using uuid) /
    # the file contains: id, parent commit, commit message, timestamp, files /
        # if parent is not null.. /
        # load the files dict from the commit.json file /
        # iterate through the dict in index.json /
        # update the files dict with the iteration /
    # file is stored in commits directory /
    # update HEAD /
    # clear index.json (staging area) /
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
    
    

def reset():
    ...


def log():
    ...

def status():
    ...

if __name__ == "__main__":
    main()