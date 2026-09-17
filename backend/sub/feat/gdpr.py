from datetime import timedelta
from discord import Message
import math

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from ..core.runtime.persistantDataManager import PersistentDataManager
from .sql.sql_serverConfig import ServerConfig
import sqlalchemy as sqla
import time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import orm
import sqlalchemy as sqla
import uuid

class SQLGPDR(DeclarativeBase):
    pass

class GDPRConsent_ServerConfig(SQLGPDR):
    __tablename__ = "feat:serverConfig:gdpr_consent"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(sqla.Uuid(), primary_key=True, default=uuid.uuid7)
    server_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer(), nullable=False)

class GDPRCommand:
    def __init__(self):
        dcClient.registerCommand("gdpr", self.onRunCommand)

    async def init(self):
        await rateLimitManager.createRateLimit("gdpr")
        detachAsync(self.onRunCommand.runForever())

        with PersistentDataManager() as db:
            SQLGPDR.metadata.create_all(db.session.get_bind())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, cmd) -> None:
        return await self._onRunCommand(message, cmd)

    async def _onRunCommand(self, message: Message, cmd: list[str]) -> None:
        userId = message.author.id

        with LogErrors('GDPRCommand'):
            if (ratelimit := await rateLimitManager.getRateLimit(userId, "gdpr")) > timedelta():
                await dcClient.runDiscord(message.reply(f"You are being rate limited. Please wait {ratelimit.seconds} seconds before trying again."))
                return

        subcmd = cmd[1].lower() if len(cmd) >= 2 else "____invalid"

        # I'm sorry.

        match subcmd:
            case "consent":
                subcmd2 = cmd[2].lower() if len(cmd) >= 3 else "____invalid"
                match subcmd2:
                    case "add":
                        target = cmd[3].lower() if len(cmd) >= 4 else "____invalid"
                        match target:
                            case "server-settings":
                                if message.author.id != message.guild.owner_id:
                                    await dcClient.runDiscord(
                                        message.reply(
                                            "Only the Guild owner can consent to collection/retention of the **Server Data > Server Configurations**"
                                            " data category (see [Privacy Policy](<https://github.com/general-software-development/CarnivoreBot/blob/main/PrivacyPolicy.md>))",
                                            delete_after=120
                                            )
                                        )
                                    return

                                with PersistentDataManager() as db:
                                    if len(db.session.scalars(
                                        sqla.select(GDPRConsent_ServerConfig).where(GDPRConsent_ServerConfig.server_id == message.guild.id)
                                    ).fetchall()) > 0:
                                        await dcClient.runDiscord(message.reply(f"You already consented to this category of data collection/retention.", delete_after=10))
                                        return

                                    consent = GDPRConsent_ServerConfig(
                                        server_id = message.guild.id
                                    )

                                    db.session.add(consent)

                                    await dcClient.runDiscord(message.reply(f"Successfully consented to the **Server Data > Server Configurations** category collection/retention. (see [Privacy Policy](<https://github.com/general-software-development/CarnivoreBot/blob/main/PrivacyPolicy.md>))"))

                            case _:
                                await dcClient.runDiscord(message.reply(f"Usage: `;gdpr consent add {{server-settings}}`"))

                    case "withdraw":
                        target = cmd[3].lower() if len(cmd) >= 4 else "____invalid"
                        match target:
                            case "server-settings":
                                if message.author.id != message.guild.owner.id:
                                    await dcClient.runDiscord(
                                        message.reply(
                                            "Only the Guild owner can withdraw consent to collection/retention of the **Server Data > Server Configurations**"
                                            " data category (see [Privacy Policy](<https://github.com/general-software-development/CarnivoreBot/blob/main/PrivacyPolicy.md>))",
                                            delete_after=120
                                            )
                                        )
                                    return

                                with PersistentDataManager() as db:
                                    consent = db.session.scalars(sqla.select(GDPRConsent_ServerConfig).where(GDPRConsent_ServerConfig.server_id == message.guild.id)).first()
                                    if consent is None:
                                        await dcClient.runDiscord(message.reply(f"You haven't consented to this category of data collection/retention.", delete_after=10))
                                        return

                                    db.session.delete(consent)

                                    server_settings = db.session.scalars(sqla.select(ServerConfig).where(ServerConfig.server_id == message.guild.id)).all()
                                    for item in server_settings:
                                        db.session.delete(item)

                                    await dcClient.runDiscord(message.reply(f"Successfully withdrew consent to the **Server Data > Server Configurations** category collection/retention. (see [Privacy Policy](<https://github.com/general-software-development/CarnivoreBot/blob/main/PrivacyPolicy.md>))"))

                            case _:
                                await dcClient.runDiscord(message.reply(f"Usage: `;gdpr consent withdraw {{server-settings}}`"))
                    
                    case _:
                        await dcClient.runDiscord(message.reply(f"Usage: `;gdpr consent {{add|withdraw}} ...`"))

            case _:
                await dcClient.runDiscord(message.reply(f"Usage: `;gdpr {{consent}} ...`"))

        await rateLimitManager.addRateLimit(userId, "gdpr", timedelta(seconds=15))

def InitialiseGDPRCommand():
    start_feat("GDPRCommand", GDPRCommand)
