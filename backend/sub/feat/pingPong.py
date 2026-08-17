from datetime import timedelta
from discord import Message

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient

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

        await dcClient.runDiscord(message.reply("Pong!"))

        await rateLimitManager.addRateLimit(userId, "ping", timedelta(seconds=2))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
