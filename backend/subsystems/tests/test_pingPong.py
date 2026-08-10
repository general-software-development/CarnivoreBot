import asyncio
from subsystems.core import dcClient
from subsystems.feat.pingPong import PingPongCommand
from subsystems.tests.utils.mockDc import DcMessage

async def test_non_spam_1():
    dcClient.discordLoop = asyncio.get_running_loop()

    isspam = PingPongCommand()
    msg = DcMessage(f";ping")

    await isspam._onRunCommand(msg)

    msg.reply.assert_awaited_once_with("Pong!")
