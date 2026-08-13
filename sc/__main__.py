from ._utils import Args

import argparse
import sys

COMMANDS = {
    "docs": "sc.docs"
}

parser = argparse.ArgumentParser(
    prog="python -m sc",
    description="CarnivoreBot development scripts",
    add_help=False
)

parser.add_argument("script", help="The target script to run.", choices = COMMANDS)

args, remaining = parser.parse_known_args()

import importlib

module = importlib.import_module(COMMANDS[args.script])

argv = Args(raw_argv = sys.argv, argv = remaining)

module.main(argv)
