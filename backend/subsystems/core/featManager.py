from collections.abc import Coroutine
import threading
import sys
import functools as fntools
import queue
from typing import Callable
from . import logManager
import asyncio
from threading import RLock

logger = logManager.getLogger("featManager")

features = []
features_lock = RLock()

def queuedFunctionAsync():
    def decorator(fn: Callable[..., Coroutine]) -> Callable:
        fn.queue = queue.Queue()

        @fntools.wraps(fn)
        async def wrapper(*args, **kwargs):
            fn.queue.put_nowait((args, kwargs))
            if fn.queue.qsize() >= 32:
                raise Exception("Queue too big.")

        async def runForever(*args, **kwargs):
            while True:
                (args, kwargs) = await asyncio.to_thread(fn.queue.get)
                loop = asyncio.get_event_loop()
                loop.create_task(fn(*args, **kwargs))
                fn.queue.task_done()

        wrapper.runForever = runForever

        return wrapper

    return decorator

def detachAsync(cr: Coroutine) -> asyncio.Task:
    loop = asyncio.get_event_loop()
    return loop.create_task(cr)

def start_feat(name: str, target: type, daemon: bool = True) -> threading.Thread:
    if sys._is_gil_enabled():
        logger.warning("The GIL is enabled. This may result in lower multithreaded performance.")

    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        l = logManager.getLogger("featManagerWrapper")
        l.info("Initialising")
        feat = target()

        loop.create_task(feat.init())

        with features_lock:
            features.append(feat)

        l.success("Initialised")

        try:
            loop.run_forever()
        except BaseException as e:
            logger.error(e)
            if loop.is_running():
                loop.stop()
        finally:
            loop.close()

    newThread = threading.Thread(target = wrapper, name = "Feat:" + name + "Thread", daemon = daemon)
    newThread.start()

    return newThread
