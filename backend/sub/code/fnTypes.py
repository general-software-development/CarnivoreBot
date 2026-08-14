from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])

def public(fn: F) -> F:
    fn.__doc__ = f"@public\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")
    return fn

def private(fn: F) -> F:
    fn.__doc__ = f"@private\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")
    return fn

def internal(fn: F) -> F:
    fn.__doc__ = f"@internal\ndef {fn.__qualname__}: ...\n\n" + (fn.__doc__ or "")
    return fn
