# MyGit

A simplified Git implementation written in Python.

## Features

- Initialize repositories
- Stage files
- Commit Files
- Checkout Previous commits
- Check the status of the working directory

## Installation


```bash
git clone <repo-url>
cd mygit
pip install -e .
```

## Usage

```bash
mygit init

# Add some files and play around before staging them, obviously
mygit add main.py

# Commit them
mygit commit "First commit"

```

To checkout commits:

```bash
mygit checkout <commit-id>
```

Use `mygit log` to check the previous commits
Use `mygit status` to see the staged, untracked, and modified files in the working directory


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

### mygit init

When this command is used, the .mygit directory is automatically created. If it's already present, the algorithm is halted to prevent any duplicates from being made. This directory consists of the following items:
-> commits (stores commit-id.json files)
-> objects (stores hashed object files)
-> index.json (stores staged files)
-> HEAD (stores the commit ID of the current HEAD pointer)

### mygit add (files)

When files are added to the staging area, these files' contents are stored in "object" files to be stored in the objects directory in the .mygit folder. The names of these files are hashes of the files' content. Then, the name of the staged files as well as the hashed values are the stored in index.json

### mygit commit (message)

Given that there are files in the staging area, a "commit-id".json file is generated in the commits directory. This file stores the timestamp, files in that commit, parent commit ID, and the commit message. The files in that json can be ones that are from previous commits (given that they are not staged), and can be newly staged and modified ones.

### mygit checkout (commit-id)

Using these commit files, we can seamlessly switch between different commits to "time-travel". Since each commit.json stores the files the relevant commit stores, we can use these to generate the relevant files with the help of the object files in the objects/ directory. Any file in the working directory not present in commit.json is removed.

### mygit log

Since each commit file contains the parent commit id, we can loop through the commit files in a logical order to output the history of commits in the right order.

### mygit status

This command outputs the staged, modified, and untracked files. Staged files are easily identified in index.json, modified files are tracked unstaged files whose current hashes ares different from the ones in HEAD, and untracked files are neither in the staging area nor are they in any commit.




