from .dependencies import *
from . import logManager
import types

logger = logManager.getLogger("assetManager")

@lambda _: _()
class AssetManager:
    def __init__(self):
        logger.info('Initialising...')
        self.rootPath = pathlib.Path(__file__).parent.parent.parent.parent
        logger.success('Initialised')

    @cached_property
    def backendPath(self):
        logger.debug('Dereferencing backendPath')
        return self.rootPath / "backend"
    
    @cached_property
    def corePath(self):
        logger.debug('Dereferencing corePath')
        return self.backendPath / "core"
    
    @cached_property
    def settings(self):
        logger.debug('Dereferencing settings')
        try:
            with open(self.rootPath / "config.toml", 'rb') as f:
                return toml.load(f)
        except Exception as e:
            logger.critical('Failed to load settings.')
            logger.critical(e, exc_info=True, stack_info=True, stacklevel=3)

    @cached_property
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
