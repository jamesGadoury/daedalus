from argparse import ArgumentParser
from pathlib import Path
from file_ops import traverse_path_and_unzip


if __name__ == "__main__":
    cli = ArgumentParser()
    cli.add_argument("path")
    args = cli.parse_args()
    if Path(args.path).exists():
        traverse_path_and_unzip(args.path)
    else:
        print(f"input {args.path} doesn't exist.")
