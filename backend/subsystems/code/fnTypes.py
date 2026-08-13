from typing import Callable

def public(fn: Callable) -> Callable:
    fn.__doc__ = f"@public\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")

    return fn

def private(fn: Callable) -> Callable:
    fn.__doc__ = f"@private\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")

    return fn

def internal(fn: Callable) -> Callable:
    fn.__doc__ = f"@internal\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")

    return fn
