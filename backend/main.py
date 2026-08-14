from sub.core.starttime.assetManager import AssetManager
from sub.core.starttime import config as configHandler
configHandler.setConfig(AssetManager.config)

from sub.core.runtime import rateLimitManager

from sub.feat import pingPong
from sub.feat import checkIsSpam
from sub.feat import getEnv

from sub.core.starttime import mainThread

from sub.core.dc.dcClient import startClient
import discord

import asyncio
import logging

import argparse
import pytest

from sub.core.log.logManager import ColorFormatter

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
