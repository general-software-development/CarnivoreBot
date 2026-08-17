from typeguard import typechecked
from beartype import beartype

from ..starttime.config import config
from ..log.logManager import getLogger

logger = getLogger('core.runtime.typeCheck')

typecheck_simple = beartype

try:
    if not config.Runtime.TypeChecking.Beartype:
        logger.info("Disabling beartype type checking.")
        typecheck_simple = lambda fn: fn # pylint: disable=unnecessary-lambda-assignment
    else:
        logger.success("Beartype type checking enabled.")
except AttributeError:
    logger.success("Beartype type checking enabled.")

typecheck_complex = typecheck_simple

try:
    if config.Runtime.TypeChecking.Typeguard:
        typecheck_complex = typechecked
        logger.success("Typegaurd type checking enabled.")
    else:
        logger.info("Disabling typeguard type checking.")
except AttributeError:
    typecheck_complex = typechecked
    logger.success("Typegaurd type checking enabled.")

__all__ = ('typecheck_simple', 'typecheck_complex')
