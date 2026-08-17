import discord
from unittest.mock import MagicMock, AsyncMock

import random

GEN_MAX_INT = 100_000_000

class DcMessageMock(MagicMock):
    reply: AsyncMock
    content: str
    author: MagicMock
    id: int

def DcUser(username: str, display_name: str | None = None, user_id = random.randint(1, GEN_MAX_INT), is_bot: bool = False) -> MagicMock:
    user = MagicMock(spec=discord.User)

    user.name = username
    user.display_name = display_name or username
    user.id = user_id
    user.bot = is_bot

    return user

def DcMessage(content: str, message_id: int = random.randint(1, GEN_MAX_INT), author: MagicMock | None = None) -> DcMessageMock:
    message = DcMessageMock(spec=discord.Message)
    message.content = content

    message.author = author if author is not None else DcUser("author")
    message.id = message_id

    message.reply = AsyncMock()

    return message
