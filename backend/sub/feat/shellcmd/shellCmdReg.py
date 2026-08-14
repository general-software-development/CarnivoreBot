from sub.abstract.feature import CommandABC
from sub.core.feat.featManager import start_feat, queuedFunctionAsync
from sub.core.dc import dcClient

from . import cmds
from .feat_shutils import Interaction, Stdout, Stdin, Hooks

class ShellCommand(CommandABC):
    def __init__(self):
        dcClient.registerCommand("", self.onRunCommand, False)

    async def init(self):
        await super().init()

    @queuedFunctionAsync()
    async def onRunCommand(self, message, cmd):
        if not (message.content.startswith("> ") or message.content.startswith("$")):
            return

        cmd = dcClient.shlexSplit(message.content.removeprefix("> ").removeprefix("$"))

        interaction = Interaction(user=message.author, message=message)
        stdin = Stdin(read = lambda: " ".join(cmd))

        exit_code: int = 0
        stdout_text = ""
        def stdout_write(text: str) -> None:
            nonlocal stdout_text
            stdout_text += text

        stdout = Stdout(
            read = lambda: stdout_text,
            write = stdout_write
        )

        hooks = Hooks(stdin=stdin, stdout=stdout, interaction=interaction)
        args = (message.content, cmd, hooks)

        match cmd[0]:
            case 'cat':
                cmds.cat.run(*args)
            case invalidCommand:
                stdout_text = f"Invalid command: {invalidCommand}"
                exit_code = 1

        await dcClient.runDiscord(message.reply(f"""```
{stdout_text}
```
-# Exit Code: `{exit_code}`"""))

def initshellcmdreg() -> None:
    start_feat("ShellCommand", ShellCommand)
