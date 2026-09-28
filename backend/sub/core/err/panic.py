from enum import Enum
from sub.core.log.logManager import getLogger

class PC(Enum):
    BAD_MEASUREMENT = -1, "-PBAD_MEASUREMENT"

class PanicError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def panic(code: PC, msg: str, *objects) -> PanicError:
    l = getLogger("PANIC")

    prefix = f"[-{hex(abs(code.value[0]))} | {code.value[1]}]  Panic: {msg}"
    err = PanicError()

    try:
        raise err
    except PanicError:
        l.critical(prefix, *objects, exc_info=err)

    return err
