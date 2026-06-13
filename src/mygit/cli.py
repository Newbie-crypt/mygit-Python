from .helpers import *
from .repository import *

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
            checkout(args.commit_id[0])

        case "log":
            log()

        case "status":
            status() 

        case _:
            sys.exit("Unknown command")