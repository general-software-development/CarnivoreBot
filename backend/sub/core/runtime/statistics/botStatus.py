from sub.utils.obj.clsselfinit import SelfInitCls
from ..typeCheck import typecheck_simple

class StatBotStatus(SelfInitCls):
    def __init__(self):
        self.__initialised = False
        self.__errors = 0

    @property
    @typecheck_simple
    def is_initialised(self) -> bool:
        return self.__initialised

    @is_initialised.setter
    @typecheck_simple
    def is_initialised(self, status: bool) -> bool:
        self.__initialised = status
        return status

    @typecheck_simple
    def get_errors(self) -> int:
        return self.__errors

    @typecheck_simple
    def incr_errors(self, no: int = 1) -> int:
        self.__errors += no
        return self.__errors
