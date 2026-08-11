from ...core import runtimeDataManager as RDM

from typing import Callable, Any
import uuid

class CachedProperty:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, instance: object | None, owner) -> Any:
        if instance is None:
            return self

        if not (instance_uuid := getattr(instance, "_cached_property_uuid", None)):
            object.__setattr__(instance, "_cached_property_uuid", uuid.uuid4())
            instance_uuid = getattr(instance, "_cached_property_uuid", None)

        if (cached := RDM.readData(f"cache", f"{self.func.__qualname__} | {instance_uuid}")) is not None:
            return cached

        value = self.func(instance)
        RDM.writeData(f"cache", f"{self.func.__qualname__} | {instance_uuid}", value)

        return value

    def __set__(self, instance: object, value: Any) -> None:
        raise AttributeError("can't set attribute (cached property is read-only)")

if not RDM.readSubsystem("cache"):
    RDM.writeSubsystem("cache", {})
    RDM.configSubsystem("cache", maxSize=16 * 1024)  # 16 KiB
