from . import logManager

class LogErrors:
    def __init__(self, name: str = "Unknown", critical: bool = False) -> None:
        self.logger = logManager.getLogger(f"LogErrors: {name}")
        self.critical = critical

    def __enter__(self) -> None:
        return

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value != None:
            try:
                raise exc_value
            except exc_type:
                if self.critical:
                    self.logger.critical(exc_value, exc_info = True, stack_info = True, stacklevel = 3)
                else:
                    self.logger.error(exc_value, exc_info = True, stack_info = True, stacklevel = 3)

        return False
