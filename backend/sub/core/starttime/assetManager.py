import pathlib
import tomllib as toml
from typing import Any
from ..log import logManager
import types
from ...utils.cache.cache_wrapper import CachedProperty

logger = logManager.getLogger("assetManager")

@lambda _: _()
class AssetManager:
    def __init__(self):
        logger.info('Initialising...')
        self.rootPath = pathlib.Path(__file__).parent.parent.parent.parent.parent
        logger.success('Initialised')

    @CachedProperty
    def backendPath(self):
        logger.debug('Dereferencing backendPath')
        return self.rootPath / "backend"
    
    @CachedProperty
    def corePath(self):
        logger.debug('Dereferencing corePath')
        return self.backendPath / "sub" / "core"

    @CachedProperty
    def testsPath(self):
        logger.debug('Dereferencing testsPath')
        return self.backendPath / "sub" / "tests"
    
    @CachedProperty
    def settings(self):
        logger.debug('Dereferencing settings')
        try:
            with open(self.rootPath / "config.toml", 'rb') as f:
                return toml.load(f)
        except Exception as e:
            logger.critical('Failed to load settings.')
            logger.critical(e, exc_info=True, stack_info=True, stacklevel=3)

    @CachedProperty
    def config(self):
        logger.debug('Dereferencing config')
        settings = self.settings

        def to_cfg(sett: dict[str, Any]) -> types.SimpleNamespace:
            cfg = types.SimpleNamespace()
            for key, value in sett.items():
                if isinstance(value, dict):
                    setattr(cfg, key, to_cfg(value))
                else:
                    setattr(cfg, key, value)
            return cfg

        cfg = to_cfg(settings)

        return cfg
