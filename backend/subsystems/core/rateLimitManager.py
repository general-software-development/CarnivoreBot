from .logManager import getLogger
from . import runtimeDataManager as RDM
from datetime import datetime, timedelta
from typing import Any
from .logErrors import LogErrors
from .suppressErrors import SuppressErrors
from threading import RLock
import threading

ratelimit_commands = []
ratelimit_commands_lock = RLock()

async def createRateLimit(command: str) -> None:
    with ratelimit_commands_lock:
        ratelimit_commands.append(command)
    
    RDM.writeSubsystem(f"rateLimitManager:{command}", {})

async def addRateLimit(target: str | int | Any, command: str, time: timedelta) -> None:
    with SuppressErrors(), LogErrors():
        RDM.writeData(f"rateLimitManager:{command}", target, datetime.now() + time)

async def getRateLimit(target: str | int | Any, command: str) -> timedelta:
    with SuppressErrors(), LogErrors():
        targetTime = RDM.readData(f"rateLimitManager:{command}", target)

        if targetTime is None:
            return timedelta()

        if datetime.now() >= targetTime:
            return timedelta()

        timeLeft = targetTime - datetime.now() if targetTime > datetime.now() else 0

        return timeLeft
    
    return timedelta()

async def refreshRateLimits(command: str) -> bool:
    try:
        with LogErrors():
            ratelimits = RDM.readSubsystem(f"rateLimitManager:{command}")
            for (identifier, targetTime) in ratelimits.items():
                if datetime.now() >= targetTime:
                    RDM.popData(f"rateLimitManager:{command}", identifier)
            
            return True
        
    except Exception as e:
        return False

import time
import asyncio

async def newThread():
    logger = getLogger("rateLimitManager")

    while True:
        time.sleep(60)

        with ratelimit_commands_lock:
            for name in ratelimit_commands:
                logger.debug(f"Refreshing rate limits for: '{name}'")
                await refreshRateLimits(name)

if threading.current_thread() is threading.main_thread():
    threading.Thread(target=lambda: asyncio.run(newThread()), name="rateLimitManagerThread", daemon=True).start()
