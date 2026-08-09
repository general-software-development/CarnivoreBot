from subsystems.core import rateLimitManager

from subsystems.feat import pingPong
from subsystems.feat import checkIsSpam
from subsystems.feat import getEnv

from subsystems.core.dcClient import startClient
from subsystems.core.assetManager import AssetManager
import discord

import asyncio
import logging

from subsystems.core.logManager import ColorFormatter

discord.utils.setup_logging(level=logging.INFO, root=False, formatter = ColorFormatter())

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Client(intents = intents)

    pingPong.InitialisePingPongCommand()
    checkIsSpam.InitialiseCheckIsSpamCommand()
    getEnv.InitialiseGetEnvCommand()

    await startClient(bot, AssetManager.settings['Discord']['App']['Auth']['AuthToken'])
    await asyncio.Event().wait()

asyncio.run(main())
