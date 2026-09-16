from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable
from discord import Message
from sub.core.runtime.errors import BotError
from sub.core.starttime.assetManager import AssetManager

class Permissions:
    __slots__ = ()

    R = 1
    W = 2
    X = 4

    RW = 3
    RWX = 7
    RX = 5

@dataclass
class SpecificFilter:
    owner: Permissions = Permissions.R | Permissions.W | Permissions.X
    admin: Permissions = Permissions.R | Permissions.W | Permissions.X
    guild_manager: Permissions = Permissions.R | Permissions.W | Permissions.X
    bot_dev: Permissions = Permissions.R | Permissions.W | Permissions.X
    others: Permissions = Permissions.R | Permissions.W | Permissions.X
    whitelist: Permissions = Permissions.R | Permissions.W | Permissions.X
    whitelist_d: list[int] = field(default_factory=list)

    def verify(self, msg: Message, requested: Permissions, confirm_debug: bool = False) -> BotError:
        perms = self._get_permissions(msg, confirm_debug)

        missing = requested & ~perms

        if missing & Permissions.R:
            return BotError("1 No Access (R)")
        elif missing & Permissions.W:
            return BotError("2 No Access (W)")
        elif missing & Permissions.X:
            return BotError("3 No Access (X)")

        return BotError("0 Success")

    def _get_permissions(self, msg: Message, confirm_debug: bool) -> Permissions:
        author = msg.author

        if author.id == msg.guild.owner_id:
            return self.owner

        if author.guild_permissions.administrator:
            return self.admin

        if author.guild_permissions.manage_guild:
            return self.guild_manager

        if self._is_bot_dev(author.id) and confirm_debug:
            return self.bot_dev

        if self._is_whitelisted(author.id):
            return self.whitelist

        return self.others

    def _is_bot_dev(self, uid: int) -> bool:
        return uid in AssetManager.config.Bot.Admins.Users

    def _is_whitelisted(self, uid: int) -> bool:
        return uid in self.whitelist_d
