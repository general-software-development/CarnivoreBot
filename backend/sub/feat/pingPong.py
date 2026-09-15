from datetime import timedelta
from discord import Message
import math

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from ..core.runtime.persistantDataManager import PersistentDataManager
import sqlalchemy as sqla
import time

class PingPongCommand:
    def __init__(self):
        dcClient.registerCommand("ping", self.onRunCommand)

    async def init(self):
        await rateLimitManager.createRateLimit("ping")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, *_) -> None:
        return await self._onRunCommand(message)

    async def _onRunCommand(self, message: Message) -> None:
        userId = message.author.id

        with LogErrors('pingPong'):
            if (ratelimit := await rateLimitManager.getRateLimit(userId, "ping")) > timedelta():
                await dcClient.runDiscord(message.reply(f"You are being rate limited. Please wait {ratelimit.seconds} seconds before trying again."))
                return

        db_connect_avg = []
        db_read_avg = []

        for i in range(30):
            db_connect = time.perf_counter()
            with PersistentDataManager() as db:
                db_connect = time.perf_counter() - db_connect
                db_read = time.perf_counter()
                db.session.execute(
                    sqla.text("SELECT * FROM \"feat:serverConfig\" LIMIT 1")
                ).first()
                db_read = time.perf_counter() - db_read

            db_connect_avg.append(db_connect)
            db_read_avg.append(db_read)

        def ravg(d: list) -> float:
            return (
                sum(d) / len(d)
                + math.prod(d) ** (1 / len(d))
            ) / 2

        db_connect_avg = (sum(db_connect_avg) / len(db_connect_avg) * 1_000_000, ravg(db_connect_avg) * 1_000_000)
        db_read_avg = (sum(db_read_avg) / len(db_read_avg) * 1_000_000, ravg(db_read_avg) * 1_000_000)

        await dcClient.runDiscord(
            message.reply(
                "Pong!\n"
                f"SQLite3 Connection: mean=`{db_connect_avg[0]}µs` / custom-avg=`{db_connect_avg[1]}µs`\n"
                f"SQLite3 Read: mean=`{db_read_avg[0]}µs` / custom-avg=`{db_read_avg[1]}µs`"
            )
        )

        await rateLimitManager.addRateLimit(userId, "ping", timedelta(seconds=2))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
