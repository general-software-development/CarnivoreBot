from sub.feat.shellcmd import feat_shutils
from sub.core.runtime import runtimeDataManager as RDM
from sub.utils.visual.size import toHumanReadable

SPACE = "         "

def run(_: str, argv: list[str], hooks: feat_shutils.Hooks) -> int:
    match argv[1]:
        case "/info/sub/core/runtime/rdm":
            hooks.stdout.write(f"""
RDM Subsystem{SPACE} Occupied Size
---
{
    '\n'.join(
        f"{subsystem.ljust(len(f'RDM Subsystem{SPACE}'))} " + 
        f"{toHumanReadable(RDM.deepSize(data)).ljust(len(f'Occupied Size{SPACE}'))} "
    for subsystem, data in RDM.data.items())
}

RDM No. Subsystems: {len(RDM.data.keys())}
RDM Total Size: {RDM.deepSize(RDM.data)}
""".strip())
            
            return 0

        case p:
            hooks.stdout.write(f"Missing path: '{p}'")
            return 2
