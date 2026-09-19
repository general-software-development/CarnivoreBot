from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable
from discord import Message
from sub.core.err.errors import BotError
from sub.core.starttime.assetManager import AssetManager

class Permissions:
    __slots__ = ()

    N = 0
    R = 1
    W = 2
    X = 4

    RW = 3
    RX = 5
    WX = 6
    RWX = 7

@dataclass
class SpecificFilter:
    owner: Permissions = None
    admin: Permissions = None
    guild_manager: Permissions = None
    bot_dev: Permissions = None
    others: Permissions = None
    whitelist: Permissions = Permissions.R | Permissions.W | Permissions.X
    whitelist_d: list[int] = field(default_factory=list)
    all_users: Permissions = Permissions.N
    default: Permissions = Permissions.N

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

        def proc(perms: Permissions) -> Permissions:
            if perms is None:
                return self.default | self.all_users

            return perms | self.all_users

        perms = Permissions.N

        if author.id == msg.guild.owner_id:
            perms |= proc(self.owner)

        if author.guild_permissions.administrator:
            perms |= proc(self.admin)
            
        if author.guild_permissions.manage_guild:
            perms |= proc(self.guild_manager)

        if self._is_bot_dev(author.id) and confirm_debug:
            perms |= proc(self.bot_dev)

        if self._is_whitelisted(author.id):
            perms |= proc(self.whitelist)

        perms |= proc(self.others)

        return perms

    def _is_bot_dev(self, uid: int) -> bool:
        return uid in AssetManager.config.Bot.Admins.Users

    def _is_whitelisted(self, uid: int) -> bool:
        return uid in self.whitelist_d
