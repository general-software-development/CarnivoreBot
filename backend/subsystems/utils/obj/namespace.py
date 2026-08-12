import types
from typing import Any
from ..ctypeguard.ctypeguard import typechecked

@typechecked
def dict_to_namespace(sett: dict[str, Any]) -> types.SimpleNamespace:
    cfg = types.SimpleNamespace()
    for key, value in sett.items():
        if isinstance(value, dict):
            setattr(cfg, key, dict_to_namespace(value))
        else:
            setattr(cfg, key, value)
    return cfg
