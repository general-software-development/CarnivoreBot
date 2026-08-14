from discord import Message
from abc import ABC, abstractmethod
from typing import Iterable

from sub.core.feat.featManager import detachAsync

class CommandABC(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def init(self):
        detachAsync(self.onRunCommand.runForever())

    @abstractmethod
    async def onRunCommand(self, message: Message, cmd: Iterable[str]) -> None:
        ...
