import discord
from discord import app_commands
from ..log.logManager import getLogger
from ..log.logErrors import LogErrors
from ..log.suppressErrors import SuppressErrors
from ..starttime.assetManager import AssetManager
from ..runtime.typeCheck import typecheck_simple, typecheck_complex
from typing import Callable, Literal
import asyncio as aio
from collections.abc import Coroutine
import shlex
from ..starttime.mainThread import mainLoop
from sub.code import fnTypes
from sub.core.err.errors import BotError
import inspect
from typing import overload, Any

logger = getLogger("dcClient")

client: discord.Client = None
client_cmd_tree: app_commands.CommandTree = None
client_ready: aio.Event = aio.Event()

listeners = {
    'onMessage': []
}

discordLoop: aio.EventLoop = mainLoop

@fnTypes.private
async def startClient(cl: discord.Client, token: str):
    global client, client_cmd_tree
    client = cl
    client_cmd_tree = app_commands.CommandTree(client)
    client_ready.set()

    client.event(on_ready)
    client.event(on_message)

    with LogErrors('dcClient', True):
        logger.debug("Starting bot...")
        await client.start(token)

@fnTypes.internal
async def on_ready():
    global client_cmd_tree
    priority_guild_ids = [1338486040683483150]
    for guild_id in priority_guild_ids:
        #await client_cmd_tree.sync(guild = guild_id)
        #logger.success(f"Synced slash commands for guild {guild_id}")
        pass

    logger.success(f"Started bot: {client.user.name} (#{client.user.id})")

    logger.debug("Syncing command tree globally...")
    synced = await client_cmd_tree.sync()
    logger.success(f"Synced command tree globally ({len(synced)} commands)!")

@fnTypes.internal
async def on_message(message: discord.Message):
    success = False

    for listener in listeners['onMessage']:
        with SuppressErrors():
            with LogErrors('dcClient:on_message'):
                if await listener(message):
                    success = True

    if not success:
        pass

@fnTypes.private
def shlexSplit(msg: str) -> list[str]:
    try:
        return shlex.split(msg, False, True)
    except Exception:
        return msg.split(" ")

@fnTypes.internal
@typecheck_simple
def isCommand(msg: str, cmd: str, prefix: str = "") -> bool:
    if cmd == "":
        return msg.startswith(prefix)

    if not msg.startswith(prefix):
        return False

    if not (msg.startswith(f"{prefix}{cmd} ") or msg == f"{prefix}{cmd}"):
        return False

    return True

@fnTypes.public
@typecheck_complex
def registerCommand(cmd: str, handler: Callable[[discord.Message, list[str]], Coroutine], includePrefix: bool = True):
    logger.debug(f"Registered command: '{cmd}'. Prefix: {'enabled' if includePrefix else 'disabled'}")

    async def wrapper(message: discord.Message):
        prefix = AssetManager.settings['Discord']['Command']['Prefix'] if includePrefix else ''

        if not isCommand(message.content, cmd, prefix):
            return False

        #logger.debug(f"Command {prefix}{cmd} was called: '{message.content}'")

        try:
            await handler(message, shlexSplit(message.content))
        except Exception as e:
            logger.exception(e)
            err = BotError("-1 Internal Error", description=str(e))
            await runDiscord(message.reply(err.to_dc()))

        return True

    listeners['onMessage'].append(wrapper)

def registerSlashCommand(cmd: str, handler: Callable[[discord.Message | None, list[str], discord.Interaction], Coroutine], description: str = None, defaults: dict[str, Any] = None, **args: type):
    defaults = defaults if defaults is not None else {}
    
    async def callback(interaction: discord.Interaction, **kwargs):
        msg = interaction.message
        split_msg = [f"/{cmd}"]
        split_msg.extend(list(kwargs.values()))
        await handler(msg, split_msg, interaction)

    callback.__signature__ = inspect.Signature([
        inspect.Parameter(
            "interaction",
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=discord.Interaction
        ),
        *[
            inspect.Parameter(
                name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=type_,
                default=defaults.get(name, inspect._empty)
            )
            for name, type_ in args.items()
        ]
    ])

    async def _register():
        await client_ready.wait()
        client_cmd_tree.add_command(
            app_commands.Command(
                name = cmd,
                description = description if description is not None else "(No description)",
                callback=callback
            )
        )

    runDiscord(_register())

@overload
async def reply(
    target: discord.Message,
    content: str | None = None,
    **kwargs
) -> discord.Message: ...

@overload
async def reply(
    target: discord.Interaction,
    content: str | None = None,
    ephemeral: bool = False,
    **kwargs
) -> discord.Message: ...

async def reply(
    target: discord.Message | discord.Interaction,
    content: str | None = None,
    **kwargs
) -> discord.Message:
    if isinstance(target, discord.Message):
        if 'ephemeral' in kwargs.keys():
            kwargs.pop('ephemeral')

        return await target.reply(content=content, **kwargs)

    if isinstance(target, discord.Interaction):
        if not target.response.is_done():
            await target.response.send_message(
                content=content,
                **kwargs
            )
            return await target.original_response()

        return await target.followup.send(
            content=content,
            wait=True,
            **kwargs
        )

    raise TypeError(f"Unsupported target type: {type(target)}")

@fnTypes.public
@typecheck_complex
def registerHandler(event: Literal['onMessage'], handler: Callable[[discord.Message], Coroutine]):
    listeners[event].append(handler)

@fnTypes.public
@typecheck_simple
def runDiscord(cr: Coroutine) -> aio.Future:
    global discordLoop
    return aio.wrap_future(aio.run_coroutine_threadsafe(cr, discordLoop))

@fnTypes.public
@typecheck_simple
def runDiscordSync(fn: Callable) -> aio.Future:
    global discordLoop
    async def _internal_async():
        return fn()
    return aio.wrap_future(aio.run_coroutine_threadsafe(_internal_async(), discordLoop))
