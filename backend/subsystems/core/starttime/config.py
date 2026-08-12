from types import SimpleNamespace
from typeguard import typechecked

config: SimpleNamespace | None = None

@typechecked
def setConfig(newConfig: SimpleNamespace):
    global config
    config = newConfig
