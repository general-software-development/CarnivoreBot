from datetime import timedelta
from discord import Message
from typing import Any

from ..core.err.errors import BotError
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from sub.core.runtime.persistantDataManager import PersistentDataManager
from sub.core.starttime.assetManager import AssetManager
from sub.core.log.logManager import getLogger
from sub.core.runtime.permissions import Permissions as Perms, SpecificFilter
from sub.feat.gdpr import GDPRConsent_ServerConfig
from typing import Iterable
import json

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import orm
import sqlalchemy as sqla
import uuid
from .sql.sql_serverConfig import ServerConfig, SQLServerConfigBase


from typing import Literal, TypeAlias, get_args

AllowedKey: TypeAlias = Literal[
    "gh.repo-owner",
    "gh.repo-name",
]

_allowed_keys = set(get_args(AllowedKey))

async def getServerSettingValue(guild_id: int, key: AllowedKey) -> ServerConfig:
    with PersistentDataManager() as db:
        results = db.session.scalars(
            sqla.select(ServerConfig).where(ServerConfig.server_id == guild_id).where(ServerConfig.key_name == key)
        ).first()

        return results

async def getServerSettings(guild_id: int) -> list[ServerConfig]:
    with PersistentDataManager() as db:
        results = db.session.scalars(
            sqla.select(ServerConfig).where(ServerConfig.server_id == guild_id)
        ).all()

        return list(results)

class ServerConfigManager:
    def __init__(self):
        dcClient.registerCommand("config.set", self.onRunSetCommand)
        dcClient.registerCommand("config.get", self.onRunGetCommand)
        self.logger = getLogger("feat:serverConfigManager")
        self.allowed_keys = _allowed_keys
        self.filter = SpecificFilter(
            owner = Perms.W,
            admin = Perms.W,
            guild_manager=Perms.W,
            bot_dev=Perms.W,
            all_users=Perms.RX,
        )

    async def init(self):
        with PersistentDataManager() as db:
            SQLServerConfigBase.metadata.create_all(db.session.get_bind())

        detachAsync(self.onRunSetCommand.runForever())
        detachAsync(self.onRunGetCommand.runForever())

    @queuedFunctionAsync()
    async def onRunSetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        return await self._onRunSetCommand(message, cmd)

    @queuedFunctionAsync()
    async def onRunGetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        return await self._onRunGetCommand(message, cmd)

    async def _onRunSetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        with PersistentDataManager() as db:
            consent = db.session.scalars(
                sqla.select(GDPRConsent_ServerConfig).where(GDPRConsent_ServerConfig.server_id == message.guild.id)
            ).first()

            if consent is None:
                await dcClient.runDiscord(
                    message.reply(
                        "Please consent to the collection/retention of the **Server Data > Server Configurations** data category"
                        "if you are the owner of the server, else ask the owner of the server to do so:\n"
                        "```\n;gdpr consent add server-settings\n```"
                    )
                )
                return

        key = cmd[1]
        value: str = cmd[2] if len(cmd) >= 3 else None
        flags = set(cmd[3:])

        author = message.author

        err = self.filter.verify(message, Perms.RWX, "+debug" in flags)
        if err:
            err.description = "Missing required permissions: **Administrator** or **Manage Server** / **Manage Guild**."
            err.details = f"Command config.set; Executed by @{author.global_name} (<@{author.id}>)"
            await dcClient.runDiscord(message.reply(err.to_dc()))
            self.logger.debug(err.to_log())
            return

        if value is None or value == "":
            value = None
        elif value.isnumeric():
            try:
                value = float(value)
            except:
                try:
                    value = int(value)
                except:
                    pass

        if value in {"True", 'true'}: value = True
        if value in {"False", 'false'}: value = False

        value: int | str | float | bool | None = value

        if key not in self.allowed_keys:
            await dcClient.runDiscord(message.reply(f"Invalid key. Allowed keys are: `{'`, `'.join(self.allowed_keys)}`"))
            return

        with PersistentDataManager() as db:
            result = db.session.scalars(
                sqla.select(ServerConfig).where(ServerConfig.server_id == message.guild.id).where(ServerConfig.key_name == key)
            ).first()

            if result:
                if value is None:
                    self.logger.debug(f"[Server {message.guild.id}]: Deleting {key}; setting to `{json.dumps(value)}`")
                    db.session.delete(result)
                    await dcClient.runDiscord(message.reply(f"Deleted setting {result.key_name}.\n-# {err.status_code}"))
                else:
                    self.logger.debug(f"[Server {message.guild.id}]: Mutating {key} to `{json.dumps(value)}`")
                    result.value = json.dumps(value)
                    await dcClient.runDiscord(message.reply(f"Mutated setting {result.key_name} to `{json.dumps(value)}`.\n-# {err.status_code}"))
            else:
                self.logger.debug(f"[Server {message.guild.id}]: Adding {key} = {json.dumps(value)}")
                setting = ServerConfig(
                    server_id = message.guild.id,
                    key_name = key,
                    value = json.dumps(value)
                )

                db.session.add(setting)

                await dcClient.runDiscord(message.reply(f"Created setting {key} = `{json.dumps(value)}`.\n-# {err.status_code}"))

    async def _onRunGetCommand(self, message: Message, cmd: Iterable[str]) -> None:
        with PersistentDataManager() as db:
            consent = db.session.scalars(
                sqla.select(GDPRConsent_ServerConfig).where(GDPRConsent_ServerConfig.server_id == message.guild.id)
            ).first()

            if consent is None:
                await dcClient.runDiscord(
                    message.reply(
                        "Please consent to the collection/retention of the **Server Data > Server Configurations** data category"
                        "if you are the owner of the server, else ask the owner of the server to do so:\n"
                        "```\n;gdpr consent add server-settings\n```"
                    )
                )
                return

        key = cmd[1] if len(cmd) >= 2 else None

        if not key:
            results = await getServerSettings(message.guild.id)
            answer = ""

            for item in results:
                answer += f"**{item.key_name}** = `{item.value}`\n"

            await dcClient.runDiscord(message.reply(answer))
        else:
            results = await getServerSettingValue(message.guild.id, key)
            await dcClient.runDiscord(message.reply(f"**{results.key_name}** = `{results.value}`"))

def InitialiseServerConfigManager():
    start_feat("ServerConfigManager", ServerConfigManager)
