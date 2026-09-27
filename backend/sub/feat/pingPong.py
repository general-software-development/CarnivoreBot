from datetime import timedelta
from discord import Message
import math

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from ..core.runtime.persistantDataManager import PersistentDataManager, APersistentDataManager
import sqlalchemy as sqla
import time

async def arange(start_or_stop: int, stop: int | None = None):
    i = start_or_stop if stop is not None else 0
    max_i = stop if stop is not None else start_or_stop

    while i < max_i:
        yield i
        i += 1

class PingPongCommand:
    def __init__(self):
        dcClient.registerCommand("ping", self.onRunCommand)

        self.first_connect = None
        self.first_read = None

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

        if self.first_connect is None:
            self.first_connect = time.perf_counter()
            with PersistentDataManager() as db:
                self.first_connect = (time.perf_counter() - self.first_connect) * 1_000_000
                self.first_read = time.perf_counter()
                db.session.execute(
                    sqla.text("SELECT * FROM \"feat:serverConfig\" LIMIT 1")
                ).first()
                self.first_read = (time.perf_counter() - self.first_read) * 1_000_000

        for i in range(150):
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

        adb_connect_avg = []
        adb_read_avg = []

        for i in range(150):
            db_connect = time.perf_counter()
            async with APersistentDataManager() as db:
                db_connect = time.perf_counter() - db_connect
                db_read = time.perf_counter()
                (await db.session.execute(
                    sqla.text("SELECT * FROM \"feat:serverConfig\" LIMIT 1")
                )).first()
                db_read = time.perf_counter() - db_read

            adb_connect_avg.append(db_connect)
            adb_read_avg.append(db_read)

        def ravg(d: list) -> float:
            return (
                sum(d) / len(d)
                + math.prod(d) ** (1 / len(d))
            ) / 2

        db_connect_avg = (sum(db_connect_avg) / len(db_connect_avg) * 1_000_000, ravg(db_connect_avg) * 1_000_000)
        db_read_avg = (sum(db_read_avg) / len(db_read_avg) * 1_000_000, ravg(db_read_avg) * 1_000_000)
        adb_connect_avg = (sum(adb_connect_avg) / len(adb_connect_avg) * 1_000_000, ravg(adb_connect_avg) * 1_000_000)
        adb_read_avg = (sum(adb_read_avg) / len(adb_read_avg) * 1_000_000, ravg(adb_read_avg) * 1_000_000)

        await dcClient.runDiscord(
            message.reply(
                "Pong!\n"
                f"PersistentDataManager First Connection: `{self.first_connect:.2f}µs`\n"
                f"PersistentDataManager First Read: `{self.first_read:.2f}µs`\n"
                f"PersistentDataManager Connection: mean=`{db_connect_avg[0]:.2f}µs` / custom-avg=`{db_connect_avg[1]:.2f}µs`\n"
                f"PersistentDataManager Read: mean=`{db_read_avg[0]:.2f}µs` / custom-avg=`{db_read_avg[1]:.2f}µs`\n"
                f"APersistentDataManager Connection: mean=`{adb_connect_avg[0]:.2f}µs` / custom-avg=`{adb_connect_avg[1]:.2f}µs`\n"
                f"APersistentDataManager Read: mean=`{adb_read_avg[0]:.2f}µs` / custom-avg=`{adb_read_avg[1]:.2f}µs`\n"
            )
        )

        await rateLimitManager.addRateLimit(userId, "ping", timedelta(seconds=5))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
