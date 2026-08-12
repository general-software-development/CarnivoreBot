from typeguard import typechecked
from beartype import beartype

from ..starttime.config import config
from ..log.logManager import getLogger

logger = getLogger('core.runtime.typeCheck')

typecheck_simple = beartype

try:
    if config.Runtime.TypeChecking.Beartype == False:
        logger.info(f"Disabling beartype type checking.")
        typecheck_simple = lambda fn: fn
    else:
        logger.success(f"Beartype type checking enabled.")
except AttributeError:
    logger.success(f"Beartype type checking enabled.")

typecheck_complex = typecheck_simple

try:
    if config.Runtime.TypeChecking.Typeguard == True:
        typecheck_complex = typechecked
        logger.success(f"Typegaurd type checking enabled.")
    else:
        logger.info(f"Disabling typeguard type checking.")
except AttributeError:
    typecheck_complex = typechecked
    logger.success(f"Typegaurd type checking enabled.")

__all__ = ('typecheck_simple', 'typecheck_complex')
