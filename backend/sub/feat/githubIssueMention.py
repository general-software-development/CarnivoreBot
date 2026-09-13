from datetime import timedelta
from discord import Message

from ..core.log.logErrors import LogErrors
from ..core.runtime import rateLimitManager
from ..core.feat.featManager import start_feat, queuedFunctionAsync, detachAsync
from ..core.dc import dcClient

class GithubIssueMentionFeat:
    def __init__(self):
        pass

    async def init(self):
        await rateLimitManager.createRateLimit("gh-issue-mention")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: Message, *_) -> None:
        return await self._onRunCommand(message)

    async def _onRunCommand(self, message: Message) -> None:
       raise NotImplementedError(".")

def InitialiseGithubIssueMention():
    start_feat("GitHubIssueMention", GithubIssueMentionFeat)
