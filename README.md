# MyGit

A simplified Git implementation written in Python.

## Features

* Initialize repositories
* Stage files
* Commit files
* Check out previous commits
* View commit history
* Check the status of the working directory

## Installation

```bash
git clone <repo-url>
cd mygit
pip install -e .
```

## Usage

```bash
mygit init

# Add some files and modify them before staging
mygit add main.py

# Commit staged changes
mygit commit "First commit"
```

To check out a previous commit:

```bash
mygit checkout <commit-id>
```

Use `mygit log` to view commit history.

Use `mygit status` to display staged, modified, and untracked files.

## Project Structure

```text
mygit/
├── src/
│   └── mygit/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── helpers.py      # Utility functions
│       └── repository.py   # Core repository logic
├── .gitignore
├── pyproject.toml          # Project metadata and packaging
├── README.md
├── requirements.txt        # Dependencies
└── tests.py
```

## Testing

Run the test suite:

```bash
pytest tests.py
```

## Technical Details

### `mygit init`

Creates the `.mygit` directory if it does not already exist. If the repository has already been initialized, the command exits without making any changes.

The `.mygit` directory contains:

* `commits/` – stores commit metadata files (`<commit-id>.json`)
* `objects/` – stores object files containing file contents
* `index.json` – stores the staging area
* `HEAD` – stores the current commit ID

### `mygit add <files>`

Stages one or more files for the next commit.

When a file is staged:

1. Its contents are read and hashed.
2. An object file is created in `.mygit/objects/` using the hash as its filename.
3. The file path and corresponding hash are stored in `index.json`.

If an identical file has already been stored, the existing object file can be reused.

### `mygit commit <message>`

Creates a new commit from the contents of the staging area.

Each commit is stored as a `<commit-id>.json` file inside the `commits/` directory and contains:

* Commit ID
* Parent commit ID
* Commit message
* Timestamp
* Snapshot of tracked files

The snapshot may contain both:

* Newly staged files
* Files inherited from previous commits that have not been modified

After a successful commit, `HEAD` is updated to point to the new commit and the staging area is cleared.

### `mygit checkout <commit-id>`

Restores the working directory to match the specified commit.

The commit's file snapshot is loaded, and the corresponding object files are used to recreate each tracked file. Any file in the working directory that is not present in the target commit's snapshot is removed.

This allows users to switch between repository states and effectively "time-travel" through project history.

### `mygit log`

Displays commit history starting from the current `HEAD` commit.

Since every commit stores its parent commit ID, MyGit can traverse the commit chain backwards and display commits in reverse chronological order.

### `mygit status`

Displays the current state of the working directory.

Files are classified into three categories:

* **Staged** – files currently present in `index.json`
* **Modified** – tracked files whose current contents differ from the version stored in `HEAD`, and which are not staged
* **Untracked** – files that are neither staged nor tracked by the current commit

```
```
