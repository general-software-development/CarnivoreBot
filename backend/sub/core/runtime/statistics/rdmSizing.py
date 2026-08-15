from ...runtime import runtimeDataManager as RDM
from ...runtime.typeCheck import typecheck_complex, typecheck_simple
from sub.utils.obj.clsselfinit import SelfInitCls
from sub.utils.visual.size import toHumanReadable

from pydantic import BaseModel

class RDMSubsystemInfo(BaseModel):
    name: str
    size: str
    sizeui: int  # ui = unbound-integer

    entries: list[str]
    entry_sizes: dict[str, str]
    entry_sizesui: dict[str, int]

class RDMSubsystemConfig(BaseModel):
    name: str
    maxSize: int | None

class StatRDMSizing(SelfInitCls):
    def __init__(self):
        pass

    @property
    @typecheck_simple
    def totalSize(self) -> str:
        return toHumanReadable(RDM.deepSize(RDM.data))

    @property
    @typecheck_simple
    def totalSizeUi(self) -> int:
        return RDM.deepSize(RDM.data)

    @property
    @typecheck_complex
    def subsystems(self) -> tuple[RDMSubsystemInfo]:
        infos = []

        for subsystem, data in RDM.data.items():
            info = self[subsystem]
            infos.append(info)

        return tuple(infos)

    @typecheck_simple
    def __getitem__(self, subsystem: str) -> RDMSubsystemInfo:
        data = RDM.data[subsystem]
        info = RDMSubsystemInfo(
            name=subsystem,
            size=toHumanReadable(RDM.deepSize(data)),
            sizeui=RDM.deepSize(data),
            entries=data.keys(),
            entry_sizes={key: toHumanReadable(RDM.deepSize(value)) for key, value in data.items()},
            entry_sizesui={key: RDM.deepSize(value) for key, value in data.items()}
        )
        return info

class StatRDMConfig(SelfInitCls):
    def __init__(self):
        pass

    @property
    @typecheck_complex
    def subsystems(self) -> tuple[RDMSubsystemConfig]:
        subCfgs = []

        for subsystem in RDM.data.keys():
            subCfgs.append(self[subsystem])

        return subCfgs

    @typecheck_simple
    def __getitem__(self, subsystem: str) -> RDMSubsystemConfig:
        subCfg = RDMSubsystemConfig(
            name=subsystem,
            maxSize=RDM.subsystem_size_limits.get(subsystem, None)
        )
        return subCfg

__all__ = (
    'StatRDMSizing',
    'StatRDMConfig'
)
