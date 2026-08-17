import pathlib
import tomllib as toml
from typing import Any
from ..log import logManager
import types
from ...utils.cache.cache_wrapper import CachedProperty
from dataclasses import dataclass
from warnings import deprecated

logger = logManager.getLogger("assetManager")

@dataclass(slots=True, frozen=True)
class PathsAsset:
    backend: pathlib.Path
    sub: pathlib.Path
    core: pathlib.Path
    tests: pathlib.Path
    feat: pathlib.Path
    utils: pathlib.Path
    abstract: pathlib.Path
    subcode: pathlib.Path

@lambda _: _()
class AssetManager:
    def __init__(self):
        logger.info('Initialising...')
        self.rootPath = pathlib.Path(__file__).parent.parent.parent.parent.parent
        logger.success('Initialised')

    @CachedProperty
    @deprecated("Use AssetManager.paths instead")
    def backendPath(self):
        logger.debug('Dereferencing backendPath')
        return self.rootPath / "backend"

    @CachedProperty
    @deprecated("Use AssetManager.paths instead")
    def corePath(self):
        logger.debug('Dereferencing corePath')
        return self.backendPath / "sub" / "core"

    @CachedProperty
    @deprecated("Use AssetManager.paths instead")
    def testsPath(self):
        logger.debug('Dereferencing testsPath')
        return self.backendPath / "sub" / "tests"

    @CachedProperty
    def paths(self) -> PathsAsset:
        return PathsAsset(
            backend = self.rootPath / "backend",
            sub = self.rootPath / "backend" / "sub",
            core = self.rootPath / "backend" / "sub" / "core",
            tests = self.rootPath / "backend" / "sub" / "tests",
            feat = self.rootPath / "backend" / "sub" / "feat",
            utils = self.rootPath / "backend" / "sub" / "utils",
            abstract = self.rootPath / "backend" / "sub" / "abstract",
            subcode = self.rootPath / "backend" / "sub" / "code"
        )

    @CachedProperty
    def settings(self) -> dict:
        logger.debug('Dereferencing settings')
        try:
            with open(self.rootPath / "config.toml", 'rb') as f:
                return toml.load(f)
        except Exception as e:
            logger.critical('Failed to load settings.')
            logger.critical(e, exc_info=True, stack_info=True, stacklevel=3)
            return {}

    @CachedProperty
    def config(self) -> types.SimpleNamespace:
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
