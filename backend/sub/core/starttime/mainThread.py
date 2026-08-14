import asyncio as aio
import threading

mainLoop: aio.EventLoop | None = None

if threading.current_thread() == threading.main_thread():
    aio.set_event_loop(aio.new_event_loop())
    mainLoop = aio.get_event_loop()
