from discord import User, Message
from typing import Callable
from dataclasses import dataclass

@dataclass
class Stdout:
    read: Callable[[], str]
    write: Callable[[str], None]

@dataclass
class Stdin:
    read: Callable[[], str]

@dataclass
class Interaction:
    user: User
    message: Message

@dataclass
class Hooks:
    stdin: Stdin
    stdout: Stdout
    interaction: Interaction
