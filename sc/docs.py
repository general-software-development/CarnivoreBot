import subprocess
import argparse
import pathlib
from ._utils import Args

def main(argv: Args):
    argparser = argparse.ArgumentParser(
        prog="python -m sc docs",
        description="CarnivoreBot Documentation"
    )
    argparser.add_argument("page", type=str, default="subsystems", choices=['subsystems', 'feat', 'abstract', 'core'], help="Documentation page to open")
    argparser.add_argument("section", type=int, default=1, nargs="?", help="man page section (default 1)")

    args = argparser.parse_args(argv.argv)

    root_path = pathlib.Path(__file__).parent.parent

    subprocess.run(["man", root_path / "cdocs" / "man" / f"{args.page}.{args.section}"], check=True)
