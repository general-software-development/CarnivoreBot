from ..abstract.feature import CommandABC
from ..core.dc import dcClient
from ..core.log.logManager import getLogger
from ..core.runtime import runtimeDataManager as RDM
from ..core.starttime.assetManager import AssetManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from sub.utils.visual import size
from sub.utils.visual.size import toHumanReadable

# For statistics
import os
import sys
import threading
import torch
import psutil
from sub.core.runtime.statistics import rdmSizing

import gc
import discord

class GetEnvCommand(CommandABC):
    def __init__(self):
        dcClient.registerCommand("getEnv", self.onRunCommand)
        dcClient.registerSlashCommand("getenv", self.onRunSlashCommand, "(Bot Dev) Get environment details", defaults=dict(hide=True, collect_garbage=True, show_threads=True, show_rdm=True, ignore_asyncio_threads=True),
                                      hide=bool, collect_garbage=bool, show_threads=bool, show_rdm=bool, ignore_asyncio_threads=bool)
        self.logger = getLogger("getEnv")
        self.authedUsers = []

    async def init(self):
        try:
            self.authedUsers = AssetManager.config.Bot.Command.getEnv.AuthedUsers
        except AttributeError:
            pass

        detachAsync(self.onRunCommand.runForever())
        detachAsync(self.onRunSlashCommand.runForever())

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

    @queuedFunctionAsync()
    async def onRunSlashCommand(self, message, cmd, interaction: dcClient.discord.Interaction):
        if interaction.user.id not in self.authedUsers:
            await dcClient.runDiscord(interaction.followup.send("No Access.", ephemeral=True))
            return

        if cmd[1]:
            gc.collect()
            self.logger.success("Performed manual garbage collection")

        mem_info = psutil.Process(os.getpid()).memory_info()

        rdm_data = ""

        if cmd[3]:
            rdm_data = "\n\n"
            for name, subsystem in RDM.data.items():
                rdm_data += f"* RDM Subsystem: `{name}`\n"
                rdm_data += f"    * Size: {RDM.deepSize(subsystem)}\n    * Nr. of Entries: {len(subsystem.items())}\n"

        embed = discord.Embed(color = discord.Color.blue(), title = "Environment Details", description=f"""**Python Version:** `{sys.version!r}`
**Total Resident Memory Used:** `{size.toHumanReadable(mem_info.rss)}`
**Total Virtual Memory Used:** `{size.toHumanReadable(mem_info.vms)}`
**Total Resident VRAM Used:** `{size.toHumanReadable(torch.cuda.memory_allocated()) if torch.cuda.is_available() else "-1B"}`
**Total Virtual VRAM Used:** `{size.toHumanReadable(torch.cuda.memory_reserved()) if torch.cuda.is_available() else "-1B"}`

# Garbage Collection Data

**Total objects:** `{len(gc.get_objects()):,}`
**Generation 0:** `{len(gc.get_objects(0)):,}`
**Generation 1:** `{len(gc.get_objects(1)):,}`
**Generation 2:** `{len(gc.get_objects(2)):,}`

# RDM

**Total size:** `{rdmSizing.StatRDMSizing.totalSize!r}`{rdm_data}
""")

        no_fields = 0

        if cmd[4]:
            for thread in threading.enumerate():
                if cmd[5] and thread.name.startswith("asyncio_"):
                    continue
                no_fields += 1
                embed.add_field(name=f"Thread `{thread.name}`",
value=f"""Name: `{thread.name}`
Ident: `{thread.ident}`
Native ID: `{thread.native_id}`""")

        print("fields: ", no_fields)

        await dcClient.runDiscord(interaction.response.send_message(embed=embed))

def InitialiseGetEnvCommand():
    start_feat("GetEnv", GetEnvCommand)
