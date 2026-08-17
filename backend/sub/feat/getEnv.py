from ..abstract.feature import CommandABC
from ..core.dc import dcClient
from ..core.starttime.assetManager import AssetManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from sub.utils.visual import size
from ..core.log.logManager import getLogger
from ..core.runtime import runtimeDataManager as RDM
from sub.utils.visual.size import toHumanReadable

# For statistics
import torch
import threading
import psutil
import os
import sys
from sub.core.runtime.statistics import rdmSizing

import gc

class GetEnvCommand(CommandABC):
    def __init__(self):
        dcClient.registerCommand("getEnv", self.onRunCommand)
        self.logger = getLogger("getEnv")
        self.authedUsers = []

    async def init(self):
        try:
            self.authedUsers = AssetManager.config.Bot.Command.getEnv.AuthedUsers
        except AttributeError:
            pass

        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message, cmd):
        if message.author.id not in self.authedUsers:
            await dcClient.runDiscord(message.reply("No Access."))
            return

        if "!gc-clean" not in cmd:
            gc.collect()
            self.logger.success("Performed manual garbage collection")

        mem_info = psutil.Process(os.getpid()).memory_info()

        def format_thread_1(thread: threading.Thread):
            return f" - Thread-Name: {thread.name!r}\n   Ident: {thread.ident}\n   Thread-ID: {thread.native_id}\n" if thread.is_alive() else ""

        text = f"""
```yaml
Python-Version: {sys.version!r}

Total-Resident-Memory-Used: "{size.toHumanReadable(mem_info.rss)}"  # RSS
Total-Virtual-Memory-Used: "{size.toHumanReadable(mem_info.vms)}"   # VMS
Total-Resident-VRAM-Used: "{size.toHumanReadable(torch.cuda.memory_allocated()) if torch.cuda.is_available() else "-1B"}" # Allocated
Total-Virtual-VRAM-Used: "{size.toHumanReadable(torch.cuda.memory_reserved()) if torch.cuda.is_available() else "-1B"}"   # Reserved
\
{("\nThreads: \n" + ''.join([format_thread_1(t) for t in threading.enumerate()]) + "\n") if "!thread" not in cmd else ""}\

GC-No-Tracked-Objects:
 - Total: {len(gc.get_objects()):,}
 - Generation-0: {len(gc.get_objects(0)):,}
 - Generation-1: {len(gc.get_objects(1)):,}
 - Generation-2: {len(gc.get_objects(2)):,}
"""

        if "!rdm" not in cmd:
            text += f"""
RDM-Total-Size: {rdmSizing.StatRDMSizing.totalSize!r}
RDM-Subsystems:"""

            for subsystem, data in RDM.data.items():
                text += f"""
 - Name: {subsystem!r}
   Size: {toHumanReadable(RDM.deepSize(data))!r}
   Entries: {('\n    - ' + '\n    - '.join([
       f"Name: {key!r}\n      Size: {toHumanReadable(RDM.deepSize(value))!r}" for key, value in data.items()
   ])) if len(data.values()) >= 1 else '[]'}"""

        text += "\n```"

        await dcClient.runDiscord(message.reply(text))

def InitialiseGetEnvCommand():
    start_feat("GetEnv", GetEnvCommand)
