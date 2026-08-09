from ..abstract.feature import CommandABC
from ..core import dcClient
from ..core.assetManager import AssetManager
from ..core.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.visual import size
from ..core.logManager import getLogger

# For statistics
import torch
import threading
import psutil
import os
import sys

import gc

class GetEnvCommand(CommandABC):
    def __init__(self):
        dcClient.registerCommand("getEnv", self.onRunCommand)
        self.logger = getLogger("getEnv")

    async def init(self):
        try:
            self.authedUsers = AssetManager.config.Bot.Command.getEnv.AuthedUsers
        except AttributeError:
            self.authedUsers = []

        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message):
        if message.author.id not in self.authedUsers:
            await dcClient.runDiscord(message.reply("No Access."))

        if "!gc-clean" not in message.content.split(" "):
            gc.collect()
            self.logger.success("Performed manual garbage collection")

        mem_info = psutil.Process(os.getpid()).memory_info()

        def format_thread_1(thread: threading.Thread):
            return f" - Thread-Name: {thread.name!r}\n   Ident: {thread.ident}\n   Thread-ID: {thread.native_id}\n" if thread.is_alive() else ""

        await dcClient.runDiscord(message.reply(f"""
```yaml
Python-Version: {sys.version!r}

Total-Resident-Memory-Used: "{size.toHumanReadable(mem_info.rss)}"
Total-Virtual-Memory-Used: "{size.toHumanReadable(mem_info.vms)}"
Total-Resident-VRAM-Used: "{size.toHumanReadable(torch.cuda.memory_allocated()) if torch.cuda.is_available() else "-1B"}"
Total-Virtual-VRAM-Used: "{size.toHumanReadable(torch.cuda.memory_reserved()) if torch.cuda.is_available() else "-1B"}"

Threads:
{''.join([format_thread_1(t) for t in threading.enumerate()])}

GC-No-Tracked-Objects:
 - Total: {len(gc.get_objects()):,}
 - Generation-0: {len(gc.get_objects(0)):,}
 - Generation-1: {len(gc.get_objects(1)):,}
 - Generation-2: {len(gc.get_objects(2)):,}
```
""".strip()))

def InitialiseGetEnvCommand():
    start_feat("GetEnv", GetEnvCommand)
