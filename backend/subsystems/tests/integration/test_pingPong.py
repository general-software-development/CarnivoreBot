import asyncio
import time
from subsystems.core import dcClient
from subsystems.feat.pingPong import PingPongCommand
from subsystems.tests.utils.mockDc import DcMessage
from subsystems.core import runtimeDataManager as RDM

import pytest

class TestReply:
    async def test_reply_noratelimit(self):
        RDM.writeSubsystem("rateLimitManager:ping", {})

        dcClient.discordLoop = asyncio.get_running_loop()

        isspam = PingPongCommand()
        msg = DcMessage(f";ping")

        await isspam._onRunCommand(msg)

        msg.reply.assert_awaited_once_with("Pong!")

    async def test_reply_ratelimit(self):
        RDM.writeSubsystem("rateLimitManager:ping", {})

        dcClient.discordLoop = asyncio.get_running_loop()

        isspam = PingPongCommand()
        msg = DcMessage(f";ping")

        await isspam._onRunCommand(msg)

        msg.reply.assert_awaited_once_with("Pong!")

        await isspam._onRunCommand(msg)

        reply_text = msg.reply.await_args.args[0]

        reply_text.startswith(f"You are being rate limited.")

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
        msg = DcMessage(f";ping")

        start = time.time()
        
        await isspam._onRunCommand(msg)
        
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000
