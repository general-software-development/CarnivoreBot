import asyncio
import time
from sub.core.dc import dcClient
from sub.feat.pingPong import PingPongCommand
from sub.tests.utils.mockDc import DcMessage
from sub.core.runtime import runtimeDataManager as RDM

import pytest

class TestReply:
    async def test_reply_noratelimit(self):
        RDM.writeSubsystem("rateLimitManager:ping", {})

        dcClient.discordLoop = asyncio.get_running_loop()

        isspam = PingPongCommand()
        msg = DcMessage(";ping")

        await isspam._onRunCommand(msg)

        msg.reply.assert_awaited_once_with("Pong!")

    async def test_reply_ratelimit(self):
        RDM.writeSubsystem("rateLimitManager:ping", {})

        dcClient.discordLoop = asyncio.get_running_loop()

        isspam = PingPongCommand()
        msg = DcMessage(";ping")

        await isspam._onRunCommand(msg)

        msg.reply.assert_awaited_once_with("Pong!")

        await isspam._onRunCommand(msg)

        reply_text = msg.reply.await_args.args[0]

        reply_text.startswith("You are being rate limited.")

class TestDelay:
    @pytest.mark.parametrize(["maxDelayMs"], [
        [1000],
        [500],
        [200],
        [100],
        [30],
        [10],
        [1]
    ])
    async def test_max_delay(self, maxDelayMs: int | float):
        RDM.writeSubsystem("rateLimitManager:ping", {})
        
        dcClient.discordLoop = asyncio.get_running_loop()
        
        isspam = PingPongCommand()
        msg = DcMessage(";ping")

        start = time.time()
        
        await isspam._onRunCommand(msg)
        
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000
