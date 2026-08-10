from ..core import logManager
from ..core.suppressErrors import SuppressErrors
from ..core.logErrors import LogErrors
from ..core.assetManager import AssetManager
from ..core import rateLimitManager
from ..core.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core import dcClient

from datetime import datetime, timedelta

from discord import Message

class PingPongCommand:
    def __init__(self):
        dcClient.registerCommand("ping", self.onRunCommand)

    async def init(self):
        await rateLimitManager.createRateLimit("ping")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, *args) -> None:
        return await self._onRunCommand(message)

    async def _onRunCommand(self, message: Message) -> None:
        userId = message.author.id

        await rateLimitManager.refreshRateLimits("ping")

        with LogErrors('pingPong'):
            if (ratelimit := await rateLimitManager.getRateLimit(userId, "ping")) > timedelta():
                await dcClient.runDiscord(message.reply(f"You are being rate limited. Please wait {ratelimit.seconds} seconds before trying again."))
                return

        await dcClient.runDiscord(message.reply("Pong!"))

        await rateLimitManager.addRateLimit(userId, "ping", timedelta(seconds=2))

def InitialisePingPongCommand():
    start_feat("PingPong", PingPongCommand)
