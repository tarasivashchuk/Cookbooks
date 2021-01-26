import time
from pathlib import Path
from typing import List


def select_files(path: Path, extension: str) -> List[Path]:
    return [f for f in path.glob(f"*.{extension}")]


def parse_path_arg():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        f"--root",
        type=str,
        required=True,
        help=f"Path to a file or directory to search for files",
    )
    parser.add_argument(
        f"--output",
        type=str,
        required=False,
        help=f"Path to save the output file at",
    )
    return parser.parse_args()


def timer(func):
    def inner():
        start = time.time()
        func()
        print(f"Took {time.time() - start:.2f} seconds!")

    return inner
