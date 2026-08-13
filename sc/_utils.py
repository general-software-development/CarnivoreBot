from dataclasses import dataclass

@dataclass
class Args:
    raw_argv: list[str]
    argv: list[str]
