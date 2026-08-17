import sys
import asyncio
import logging
import argparse
import pytest
import discord

from sub.core.starttime.assetManager import AssetManager
from sub.core.starttime import config as configHandler
configHandler.setConfig(AssetManager.config)

from sub.feat import pingPong
from sub.feat import checkIsSpam
from sub.feat import getEnv
from sub.feat.shellcmd import shellcmd

from sub.core.starttime import mainThread

from sub.core.dc.dcClient import startClient

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
    shellcmd.InitShellCmd()

    await startClient(bot, AssetManager.settings['Discord']['App']['Auth']['AuthToken'])

    await asyncio.Event().wait()

if args.tests:
    sys.exit(pytest.main(["-v", AssetManager.testsPath]))

mainThread.mainLoop.run_until_complete(main())
