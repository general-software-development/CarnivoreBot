from subsystems.core import rateLimitManager

from subsystems.feat import pingPong
from subsystems.feat import checkIsSpam
from subsystems.feat import getEnv

from subsystems.core import mainThread

from subsystems.core.dcClient import startClient
from subsystems.core.assetManager import AssetManager
import discord

import asyncio
import logging

import argparse
import pytest

from subsystems.core.logManager import ColorFormatter

discord.utils.setup_logging(level=logging.INFO, root=False, formatter = ColorFormatter())

argParser = argparse.ArgumentParser()
argParser.add_argument("--tests", action="store_true")

args = argParser.parse_args()

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Client(intents = intents)

    pingPong.InitialisePingPongCommand()
    checkIsSpam.InitialiseCheckIsSpamCommand()
    getEnv.InitialiseGetEnvCommand()

    await startClient(bot, AssetManager.settings['Discord']['App']['Auth']['AuthToken'])

    await asyncio.Event().wait()

if args.tests:
    exit(pytest.main(["-v", AssetManager.testsPath]))

mainThread.mainLoop.run_until_complete(main())
