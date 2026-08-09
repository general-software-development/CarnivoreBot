import discord
from .logManager import getLogger
from .logErrors import LogErrors
from .assetManager import AssetManager
from typing import Callable, Coroutine, Literal
import asyncio as aio
from collections.abc import Coroutine

logger = getLogger("dcClient")

client: discord.Client = None

listeners = {
    'onMessage': []
}

discordLoop: aio.EventLoop = None

async def startClient(cl: discord.Client, token: str):
    global client
    client = cl

    client.event(on_ready)
    client.event(on_message)

    global discordLoop
    discordLoop = aio.get_event_loop()
    
    with LogErrors('dcClient', True):
        logger.debug("Starting bot...")
        await client.start(token)

#@client.event
async def on_ready():
    logger.success(f"Started bot: {client.user.name} (#{client.user.id})")

async def on_message(message: discord.Message):
    success = False

    for listener in listeners['onMessage']:
        with LogErrors('dcClient:on_message'):
            if await listener(message):
                success = True

    if success == False:
        ...
        # logger.debug(f"Skipped over command in message: '{message.content}'. Cause: no handler installed")

def registerCommand(cmd: str, handler: Callable[[discord.Message], Coroutine], includePrefix: bool = True):
    logger.debug(f"Registered command: '{cmd}'. Prefix: {'enabled' if includePrefix else 'disabled'}")

    async def wrapper(message: discord.Message):
        prefix = AssetManager.settings['Discord']['Command']['Prefix'] if includePrefix else ''
        
        if not message.content.startswith(prefix):
            return False
        
        if not message.content.startswith(f"{prefix}{cmd}"):
            return False
        
        logger.info(f"Command {prefix}{cmd} was called: '{message.content}'")

        await handler(message)

        return True
        
    listeners['onMessage'].append(wrapper)

def registerHandler(event: Literal['onMessage'], handler: Callable[[discord.Message], Coroutine]):
    listeners[event].append(handler)

def runDiscord(cr: Coroutine) -> aio.Future:
    global discordLoop
    return aio.wrap_future(aio.run_coroutine_threadsafe(cr, discordLoop))
