from sub.core.feat.featManager import queuedFunctionAsync, start_feat, detachAsync
from sub.core.dc import dcClient as dc
from ..abstract.feature import CommandABC
from sub.core.log.logManager import getLogger
from sub.core.log.logErrors import LogErrors
from sub.core.log.suppressErrors import SuppressErrors
from sub.core.runtime.permissions import SpecificFilter, Permissions
from sub.core.err.errors import BotError
from sub.core.runtime.persistantDataManager import PersistentDataManager

import discord

class AdminCommand(CommandABC):
    def __init__(self):
        dc.registerCommand("admin", self.onRunCommand, True)
        self.logger = getLogger("admin_cmd")
        self.filter = SpecificFilter(
            default=Permissions.N,
            all_users=Permissions.N,
            whitelist=Permissions.N,
            bot_dev=Permissions.RWX
        )

    async def init(self):
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: discord.Message, cmd):
        if len(cmd) >= 2 and cmd[1] in {"whitelist"}:
            with SuppressErrors(), LogErrors("admin_cmd", stack_info=False):
                return await self._onRunActualCommand(message, cmd)

        with SuppressErrors(), LogErrors("admin_cmd", stack_info=False):
            return await self._onRunCommand(message)
    
    async def _onRunCommand(self, message: discord.Message):

        err = self.filter.verify(message, Permissions.X, True)
        if err:
            await dc.runDiscord(message.reply(err.to_dc()))
            raise err

        await dc.runDiscord(message.reply(f"Usage: admin {{whitelist}}.\n-# Note: this is an admin-only command."))
    
    async def _onRunActualCommand(self, message: discord.Message, cmd):
        err = self.filter.verify(message, Permissions.X, True)
        if err:
            await dc.runDiscord(message.reply(err.to_dc()))
            raise err

        subcmd = None
        
        with SuppressErrors(), LogErrors("admin_cmd"):
            subcmd = cmd[1]

        match subcmd:
            case "whitelist":
                ...

    async def _whitelistCommand(self, msg: discord.Message, cmd: list[str]) -> BotError:
        if len(cmd) != 3:
            await dc.runDiscord(msg.reply(f"Usage: `admin whitelist +<userid>` `admin whitelist -<userid>` `admin whitelist <userid>` `admin whitelist *`"))

        action = cmd[2]

        if action == '*':
            with PersistentDataManager() as db:
                

        return BotError("0 Success")

def InitialiseAdminCommand():
    start_feat("AdminCommand", AdminCommand)
