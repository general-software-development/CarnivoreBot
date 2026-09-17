from datetime import timedelta
from discord import Message
import discord
import httpx
import pprint
import json
import io

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from .serverConfig import getServerSettingValue


import tempfile
import pypandoc
import os

# AI-Generated Function
def markdown_to_pdf(markdown_text: str) -> bytes:
    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False,
    ) as tmp:
        pdf_path = tmp.name

    try:
        pypandoc.convert_text(
            markdown_text,
            to="pdf",
            format="gfm",
            outputfile=pdf_path,
            extra_args=[
                "--pdf-engine=typst",

                "--variable-json",
                'margin={"x":"20mm","y":"20mm"}',

                "-V",
                "papersize=a4",
            ],
        )

        with open(pdf_path, "rb") as file:
            return file.read()

    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

class GetDocument:
    def __init__(self):
        dcClient.registerCommand("legal", self.onRunCommand, True)

        self.license_cache = None
        self.privacy_cache = None

    async def init(self):
        await rateLimitManager.createRateLimit("legal-cmd")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, cmd) -> None:
        return await self._onRunCommand(message, cmd)

    async def _onRunCommand(self, message: Message, cmd: list[str]) -> None:
        if (ratelimit := await rateLimitManager.getRateLimit(message.author.id, "legal-cmd")) > timedelta():
            await dcClient.runDiscord(message.reply(f"You are being rate limited. Please wait {ratelimit.seconds} seconds before trying again."))
            return

        target = cmd[1] if len(cmd) >= 2 else None
        if not target: target = None

        if target is None:
            await dcClient.runDiscord(message.reply(f"Missing document name. Document names: `privacy`, `license`."))
            return

        url = None
        if target.lower() == "privacy":
            url = "https://raw.githubusercontent.com/general-software-development/CarnivoreBot/refs/heads/main/PrivacyPolicy.md"
        elif target.lower() == "license":
            url = "https://raw.githubusercontent.com/general-software-development/CarnivoreBot/refs/heads/main/LICENSE.md"
        else:
            await dcClient.runDiscord(message.reply(f"Invalid document name. Document names: `privacy`, `license`."))
            return

        await rateLimitManager.addRateLimit(message.author.id, "legal-cmd", timedelta(seconds=2))

        if target.lower() == "privacy" and self.privacy_cache:
            await dcClient.runDiscord(message.reply(self.privacy_cache))
        elif target.lower() == "license" and self.license_cache:
            await dcClient.runDiscord(message.reply(self.license_cache))
        else:
            async with httpx.AsyncClient() as cl:
                response = await cl.get(url)
                response.raise_for_status()

                md_data = response.content.decode(errors="replace")

                pdf_data = markdown_to_pdf(md_data)

                name = target.lower()

                message = await dcClient.runDiscord(message.reply(
                    file=discord.File(
                        io.BytesIO(pdf_data),
                        filename=f"{name}.pdf",
                    )
                ))

                attachment = message.attachments[0]
                att_url = attachment.url

                if target.lower() == "privacy":
                    self.privacy_cache = att_url
                elif target.lower() == "license":
                    self.license_cache = att_url

def InitialiseGetLegalDocument():
    start_feat("GetLegalDocument", GetDocument)
