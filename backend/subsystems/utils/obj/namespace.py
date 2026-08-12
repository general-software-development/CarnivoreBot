import types
from typing import Any

def dict_to_namespace(sett: dict[str, Any]) -> types.SimpleNamespace:
    cfg = types.SimpleNamespace()
    for key, value in sett.items():
        if isinstance(value, dict):
            setattr(cfg, key, dict_to_namespace(value))
        else:
            setattr(cfg, key, value)
    return cfg
