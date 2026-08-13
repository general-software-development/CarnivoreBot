import discord
from ..log.logManager import getLogger
from ..log.logErrors import LogErrors
from ..starttime.assetManager import AssetManager
from typing import Callable, Coroutine, Literal
import asyncio as aio
from collections.abc import Coroutine
import shlex
from ..starttime.mainThread import mainLoop
from subsystems.code import fnTypes

logger = getLogger("dcClient")

client: discord.Client = None

listeners = {
    'onMessage': []
}

discordLoop: aio.EventLoop = mainLoop

@fnTypes.private
async def startClient(cl: discord.Client, token: str):
    global client
    client = cl

    client.event(on_ready)
    client.event(on_message)
    
    with LogErrors('dcClient', True):
        logger.debug("Starting bot...")
        await client.start(token)

@fnTypes.internal
async def on_ready():
    logger.success(f"Started bot: {client.user.name} (#{client.user.id})")

@fnTypes.internal
async def on_message(message: discord.Message):
    success = False

    for listener in listeners['onMessage']:
        with LogErrors('dcClient:on_message'):
            if await listener(message):
                success = True

    if success == False:
        ...

@fnTypes.private
def shlexSplit(msg: str) -> list[str]:
    try:
        return shlex.split(msg, False, True)
    except:
        return msg.split(" ")

@fnTypes.public
def registerCommand(cmd: str, handler: Callable[[discord.Message, list[str]], Coroutine], includePrefix: bool = True):
    logger.debug(f"Registered command: '{cmd}'. Prefix: {'enabled' if includePrefix else 'disabled'}")

    async def wrapper(message: discord.Message):
        prefix = AssetManager.settings['Discord']['Command']['Prefix'] if includePrefix else ''
        
        if not message.content.startswith(prefix):
            return False
        
        if not message.content.startswith(f"{prefix}{cmd}"):
            return False
        
        logger.info(f"Command {prefix}{cmd} was called: '{message.content}'")

        await handler(message, shlexSplit(message.content))

        return True
        
    listeners['onMessage'].append(wrapper)

@fnTypes.public
def registerHandler(event: Literal['onMessage'], handler: Callable[[discord.Message], Coroutine]):
    listeners[event].append(handler)

@fnTypes.public
def runDiscord(cr: Coroutine) -> aio.Future:
    global discordLoop
    return aio.wrap_future(aio.run_coroutine_threadsafe(cr, discordLoop))
