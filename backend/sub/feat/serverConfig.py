from datetime import timedelta
from discord import Message
import discord
import httpx
import pprint

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from sub.core.runtime.persistantDataManager import PersistentDataManager
from sub.core.starttime.assetManager import AssetManager
from sub.core.log.logManager import getLogger
from typing import Iterable
import json

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import orm
import sqlalchemy as sqla
import uuid

class SQLServerConfigBase(DeclarativeBase):
    pass

class ServerConfig(SQLServerConfigBase):
    __tablename__ = "feat:serverConfig"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(sqla.Uuid(), primary_key=True, default=uuid.uuid7)
    server_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer(), nullable=False)
    key_name: orm.Mapped[str] = orm.mapped_column(sqla.String(50), nullable=False)
    value: orm.Mapped[str] = orm.mapped_column(sqla.String(500), nullable=True)

class ServerConfigManager:
    def __init__(self):
        dcClient.registerCommand("config.set", self.onRunSetCommand)
        dcClient.registerCommand("config.get", self.onRunGetCommand)
        self.logger = getLogger("feat:serverConfigManager")
        self.allowed_keys = {
            "gh.repo-owner",
            "gh.repo-name"
        }

    async def init(self):
        with PersistentDataManager() as db:
            SQLServerConfigBase.metadata.create_all(db.session.get_bind())

        detachAsync(self.onRunSetCommand.runForever())

    @queuedFunctionAsync()
    async def onRunSetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        return await self._onRunSetCommand(message, cmd)

    @queuedFunctionAsync()
    async def onRunGetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        #return await self._onRunGetCommand(message)
        return

    async def _onRunSetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        key = cmd[1]
        value: str = cmd[2]
        flags = set(cmd[3:])

        if value.isnumeric():
            try:
                value = float(value)
            except:
                try:
                    value = int(value)
                except:
                    pass

        if value in {"True", 'true'}: value = True
        if value in {"False", 'false'}: value = False

        value: int | str | float | bool = value
        
        author = message.author

        has_perms = author.guild_permissions.administrator or author.guild_permissions.manage_guild

        if not has_perms:
            if not ("+debug" in flags and author.id in AssetManager.config.Bot.Admins.Users):
                await dcClient.runDiscord(message.reply(f"You do not have the required permissions to run this command. This command requires either the **Administrator** permission or the **Manage Server** / **Manage Guild** permission."))
                self.logger.debug(f"User @{author.global_name} ({author.id}) attempted to run privileged command config.set without sufficient permissions.")
                return

        if key not in self.allowed_keys:
            await dcClient.runDiscord(message.reply(f"Invalid key. Allowed keys are: `{'`, `'.join(self.allowed_keys)}`"))
            return

        with PersistentDataManager() as db:
            result = db.session.scalars(
                sqla.select(ServerConfig).where(ServerConfig.server_id == message.guild.id).where(ServerConfig.key_name == key)
            ).first()

            if result:
                self.logger.debug(f"[Server {message.guild.id}]: Mutating {key} to `{json.dumps(value)}`")
                result.value = json.dumps(value)
            else:
                self.logger.debug(f"[Server {message.guild.id}]: Adding {key} = {json.dumps(value)}")

                setting = ServerConfig(
                    server_id = message.guild.id,
                    key_name = key,
                    value = json.dumps(value)
                )
                db.session.add(setting)

    async def _onRunGetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        key = cmd[1] if len(cmd) >= 2 else None

        with PersistentDataManager() as db:
            if not key:
                results = list(db.session.scalars(
                    sqla.select(ServerConfig)
                ).all())

                answer = ""

                for item in results:
                    answer += f"**{item.key_name}** = `{item.value}`"

                await dcClient.runDiscord(message.reply(answer))

def InitialiseServerConfigManager():
    start_feat("ServerConfigManager", ServerConfigManager)
