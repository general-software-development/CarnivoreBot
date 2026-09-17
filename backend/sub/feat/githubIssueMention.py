from datetime import timedelta
from discord import Message
import discord
import httpx
import pprint
import json

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient
from .serverConfig import getServerSettingValue

class GithubIssueMentionFeat:
    def __init__(self):
        dcClient.registerCommand("", self.onRunCommand, False)

    async def init(self):
        #await rateLimitManager.createRateLimit("gh-issue-mention")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, *_) -> None:
        return await self._onRunCommand(message)

    async def _onRunCommand(self, message: Message) -> None:
        repo_name = await getServerSettingValue(message.guild.id, "gh.repo-name")
        repo_owner = await getServerSettingValue(message.guild.id, "gh.repo-owner")

        for word in message.content.replace("(", " ").replace(")", " ").replace(".", " ").replace(",", " ").strip("?!").split():
            tokens = word.split("#", maxsplit=1)

            if len(tokens) > 1:
                if tokens[1].isnumeric():
                    identifier = int(tokens[1])
                    github_url = f"https://api.github.com/repos/{json.loads(repo_owner.value)}/{json.loads(repo_name.value)}/"

                    issue_url = github_url + "issues/" + str(identifier)

                    issue_title: str = None
                    issue_body: str = None
                    is_pull_request: bool = None
                    is_closed: bool = None
                    is_locked: bool = None
                    is_merged: bool = None
                    lock_reason: str | None = None
                    closed_reason: str = None
                    html_url: str = None

                    async with httpx.AsyncClient() as cl:
                        response = await cl.get(issue_url)  
                        response.raise_for_status()

                        data: dict = response.json()
                        
                        issue_title = data['title']
                        issue_body = data['body'] or ''
                        is_pull_request = "pull_request" in data.keys()
                        is_closed = data['state'] != 'open'
                        is_locked = data['locked']
                        is_merged = bool(data.get('pull_request', {}).get('merged_at'))
                        lock_reason = data['active_lock_reason']
                        closed_reason = data['state_reason']
                        html_url = data['html_url']

                    embed = discord.Embed(
                        title=f"Issue #{identifier}: \"{issue_title}\"",
                        description=f"{issue_body[:100]}" + ('...' if len(issue_body) >= 100 else ''),
                        color = (
                            discord.Color.green() if not is_closed else
                            discord.Color.red() if closed_reason in {'duplicate', 'closed'} else  #  Issue closed as duplicate, or Pull Request closed (not merged)
                            discord.Color.from_rgb(105, 36, 255) if closed_reason == 'completed' else  # Issue closed as completed, or closed with status=null
                            discord.Color.from_rgb(105, 36, 255) if is_merged else  # Pull Request merged
                            discord.Color.from_rgb(107, 107, 107) if closed_reason == 'not_planned' else  # Issue closed as not planned
                            discord.Color.red()
                        )
                    )
                    embed.add_field(
                        name = "Issue type",
                        value = "Pull Request" if is_pull_request else "Issue"
                    )
                    embed.add_field(
                        name = "Status",
                        value = (
                            "Open" if not is_closed else
                            "PR Closed" if closed_reason == 'closed' else 
                            "Closed as Completed" if closed_reason == 'completed' else
                            "Merged" if is_merged else
                            "Closed as Not Planned" if closed_reason == 'not_planned' else
                            "Closed as Duplicate" if closed_reason == 'duplicate' else
                            "Closed"
                        )
                    )
                    embed.add_field(
                        name = "Locked status",
                        value = f"Locked for: '{lock_reason}'" if is_locked else "Not Locked"
                    )
                    embed.add_field(
                        name = "Issue URL",
                        value = html_url
                    )

                    await dcClient.runDiscord(message.reply(None, embed=embed))

def InitialiseGithubIssueMention():
    start_feat("GitHubIssueMention", GithubIssueMentionFeat)
