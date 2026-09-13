from sub.core.runtime import runtimeDataManager as RDM

from typing import Callable, Any, overload
import uuid

from beartype import beartype

class CachedProperty[T, R]:
    @beartype
    def __init__(self, func: Callable[[T], R]) -> None:
        self.func = func
        self.__doc__ = func.__doc__

    @overload
    def __get__(self, instance: None, owner: type[T]) -> "CachedProperty[T, R]":
        ...

    @overload
    def __get__(self, instance: T, owner: type[T] | None = None) -> R:
        ...

    def __get__(self, instance: T | None, owner: type[T] | None = None) -> R | "CachedProperty[T, R]":
        if instance is None:
            return self

        if not (instance_uuid := getattr(instance, "_cached_property_uuid", None)):
            object.__setattr__(instance, "_cached_property_uuid", uuid.uuid4())
            instance_uuid = getattr(instance, "_cached_property_uuid", None)

        if (cached := RDM.readData("cache", f"{self.func.__qualname__} | {instance_uuid}")) is not None:
            return cached

        value = self.func(instance)
        RDM.writeData("cache", f"{self.func.__qualname__} | {instance_uuid}", value)

        return value

    def __set__(self, instance: object, value: Any) -> None:
        raise AttributeError("can't set attribute (cached property is read-only)")

if not RDM.readSubsystem("cache"):
    RDM.writeSubsystem("cache", {})
    RDM.configSubsystem("cache", maxSize=16 * 1024)  # 16 KiB
