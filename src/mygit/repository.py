from .helpers import *

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
    

def add(paths, repo_directory='.'):

    is_repository_initialized(repo_directory=repo_directory)

    if not files_exist(paths, repo_directory=repo_directory)[0]:
        sys.exit(f"{paths[0]} does not exist.")

    for path in paths:
        path = path.replace("./","").replace(".\\", "")
        with open(f"{repo_directory}/{path}", "rb") as file:
            contents = file.read()
        hash = hashlib.sha256(contents).hexdigest()
        output_path = f"{repo_directory}/.mygit/objects/" + hash
        if not Path(output_path).exists():
            # Making the new file...
            with open(output_path, "wb") as file:
                file.write(contents)

            # Updating the index
            with open(f"{repo_directory}/.mygit/index.json", "r") as f:
                index = json.load(f)
            
            index[path] = hash

            with open(f"{repo_directory}/.mygit/index.json", "w") as f:
                json.dump(index, f, indent=4)
    

def commit(message, repo_directory='.'):
    is_repository_initialized(repo_directory=repo_directory)
    
    if empty_index(repo_directory=repo_directory):
        sys.exit("No files present in the staging area.")
    
    # Obtaining the commit parent..
    with open(f"{repo_directory}/.mygit/HEAD", 'r') as f:
        commit_parent = f.read()

    # Setting up the files to be committed..
    with open(f"{repo_directory}/.mygit/index.json", "r") as f:
        files = json.load(f)

    if commit_parent != "null":
        with open(f"{repo_directory}/.mygit/commits/{commit_parent}.json", "r") as f:
            commit_parent_json = json.load(f)

        for key in commit_parent_json["files"]:
            if key not in files:
                files[key] = commit_parent_json["files"][key]

    # Setting up the data to be stored in the commit json file
    commit_data = {
        "parent_commit": commit_parent,
        "message": message,
        "timestamp": str(datetime.datetime.now()),
        "files": files
    }

    commit_id = hashlib.sha256(json.dumps(commit_data).encode("utf-8")).hexdigest()

    # Creating the json file..
    with open(f"{repo_directory}/.mygit/commits/{commit_id}.json", 'w') as f:
        json.dump(commit_data, f, indent=4)

    # Update HEAD
    with open(f"{repo_directory}/.mygit/HEAD", 'w') as f:
        f.write(commit_id)
    
    # Clearing the staging area (index.json)
    with open(f"{repo_directory}/.mygit/index.json", 'w') as f:
        f.write("{}")

    # Returned for unit testing purposes
    return commit_id, files
    
    

def checkout(commit_id, repo_directory='.'):
    is_repository_initialized(repo_directory=repo_directory)

    # Ensuring the commit id exists..
    path = f"{repo_directory}/.mygit/commits/{commit_id}.json"

    if not Path(path).exists():
        sys.exit("Invalid Commit ID")


    # Creating/Overwriting files..
    with open(path, 'r') as f:
        contents = json.load(f)
    files = contents["files"]
    for key in files:
        with open(f"{repo_directory}/.mygit/objects/{files[key]}", "rb") as f:
            input_data = f.read()
        with open(f"{repo_directory}/{key}", "wb") as f:
            f.write(input_data)
    
    # Removing files/directories not present in the snapshot...
    current_directory_files = list(Path(repo_directory).glob("*"))
    for file in current_directory_files:
        if str(file).split('\\')[-1] not in files and ".mygit" not in str(file):
            if file.is_file():
                file.unlink()          # remove file
            elif file.is_dir():
                shutil.rmtree(file)  

    # Changing the HEAD..
    with open(f"{repo_directory}/.mygit/HEAD", 'w') as f:
        f.write(commit_id)
    
    # Clearing the staging area (index.json)
    with open(f"{repo_directory}/.mygit/index.json", 'w') as f:
        f.write("{}")
    
def log():
    ...

def status():
    ...
