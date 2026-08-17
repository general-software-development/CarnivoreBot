import asyncio
import pytest
from sub.core.dc import dcClient
from sub.feat.checkIsSpam import CheckIsSpamCommand
from sub.tests.utils.mockDc import DcMessage

@pytest.mark.parametrize(["messageContent"], [
    ["hey"],
    ["hi"],
    ["Hey, there!"],  # no one says this but whatever
    ["Hello!"],
    ["update when?"],
    ["what's <#12381381247> for"],
    ["<@28123824126> yo can you review this rq"],
    ["what's <@&1281782347>"],
    ["bro"]
])
async def test_non_spam_1(messageContent: str):
    dcClient.discordLoop = asyncio.get_running_loop()

    isspam = CheckIsSpamCommand()
    msg = DcMessage(f";is_spam {messageContent}")

    await isspam._onRunCommand(msg, dcClient.shlexSplit(msg.content))

    msg.reply.assert_awaited_once()

    reply_text = msg.reply.await_args.args[0]

    assert reply_text.startswith("NOT SPAM")

@pytest.mark.parametrize(["messageContent"], [
    ["<@28123824126> <@28123824126> <@28123824126> <@28123824126>"],
    ["""🎉 MrBeast is giving away $2,500 to 500 selected Discord members!
You've been chosen!
⏰ Claim expires in 09:47 — click here: www.mrbeast-claim2026.org/win"""]
])
async def test_spam_1(messageContent: str):
    dcClient.discordLoop = asyncio.get_running_loop()

    isspam = CheckIsSpamCommand()
    msg = DcMessage(f";is_spam {messageContent}")

    await isspam._onRunCommand(msg, dcClient.shlexSplit(msg.content))

    msg.reply.assert_awaited_once()

    reply_text = msg.reply.await_args.args[0]

    assert reply_text.startswith("SPAM")
