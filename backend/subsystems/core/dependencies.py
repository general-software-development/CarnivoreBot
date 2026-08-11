import pathlib
from functools import cached_property
import logging
import colorama
import datetime
import tomllib as toml
import sys
from typing import AnyStr, Any, Callable, Optional
import functools as fntools
import queue

def __getattr__(name: str, *_, hasAlreadyLogged = [False]):
    from ..core.logManager import getLogger
    if not hasAlreadyLogged[0]:
        logger = getLogger("core.dependencies")
        logger.warning(f"The core.dependencies model is deprecated. Please switch to importing dependencies where needed.")
        hasAlreadyLogged[0] = True

    try:
        globals()[name]
    except KeyError as e:
        raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
