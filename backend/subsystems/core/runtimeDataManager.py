from threading import RLock, Thread
import threading
from .suppressErrors import SuppressErrors
from .logErrors import LogErrors
from .logManager import getLogger
from .visual.size import toHumanReadable
from typing import Optional
from time import sleep
import sys

import copy

data: dict[str, dict[any, any]] = {}
subsystem_size_limits: dict[str, int] = {}
data_lock = RLock()

import torch
def deepSize(value: dict | list, seen: set[int] | None = None) -> int:
    if seen is None:
        seen = set()

    if id(value) in seen:
        return 0

    seen.add(id(value))

    if isinstance(value, list):
        return sum(map(lambda x: deepSize(x, seen), value)) + sys.getsizeof(value)
    elif isinstance(value, dict):
        size = sys.getsizeof(value)

        for key in value.keys():
            size += sys.getsizeof(key)

        for value in value.values():
            size += deepSize(value, seen)

        return size
    elif isinstance(value, tuple):
        return sum(map(lambda x: deepSize(x, seen), value)) + sys.getsizeof(value)
    elif isinstance(value, set):
        return sum(map(lambda x: deepSize(x, seen), value)) + sys.getsizeof(value)
    elif isinstance(value, torch.nn.Module):
        return sum(
            t.numel() * t.element_size() for t in list(value.parameters()) + list(value.buffers())
        )
    else:
        return sys.getsizeof(value)

def readData(subsystem: str, key: any) -> any:
    with data_lock:
        value = data.get(subsystem, {}).get(key)

    return value

def readSubsystem(subsystem: str) -> dict[any, any] | None:
    with data_lock:
        value = data.get(subsystem)

    return copy.deepcopy(value)

def writeSubsystem(subsystem: str, value: dict[any, any]) -> None:
    with data_lock:
        data[subsystem] = value

def writeData(subsystem: str, key: any, value: any) -> None:
    with data_lock:
        if (data.get(subsystem, None) is None):
            data[subsystem] = {}
        data[subsystem][key] = value

def popData(subsystem: str, key: any) -> None:
    with data_lock:
        if (v := data.get(subsystem)) is not None:
            with SuppressErrors(), LogErrors():
                v.pop(key)

def configSubsystem(subsystem: str, *_, maxSize: Optional[int]):
    if maxSize is not None:
        subsystem_size_limits[subsystem] = maxSize

def newThread():
    logger = getLogger("runtimeDataManager")
    while True:
        sleep(30)
        for (name, subsystem) in data.items():
            if deepSize(subsystem) >= subsystem_size_limits.get(name, 512) * 15:
                logger.critical(f"Size of runtime data subsystem '{name}' exceeds the limit of {toHumanReadable(subsystem_size_limits.get(name, 512))} by 15x (or more), currently occupying {toHumanReadable(deepSize(subsystem))}")
            elif deepSize(subsystem) >= subsystem_size_limits.get(name, 512):
                logger.warning(f"Size of runtime data subsystem '{name}' exceeds the limit of {toHumanReadable(subsystem_size_limits.get(name, 512))}, currently occupying {toHumanReadable(deepSize(subsystem))}")

if threading.current_thread() is threading.main_thread():
    Thread(target=newThread, name="runtimeDataManagerThread", daemon=True).start()
