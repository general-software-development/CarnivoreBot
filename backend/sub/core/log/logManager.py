import logging
from datetime import datetime
import colorama

logging.getLogger("werkzeug").setLevel(logging.ERROR)

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: f"{colorama.Style.DIM}{colorama.Fore.RESET}",
        logging.INFO: f"{colorama.Style.RESET_ALL}",
        SUCCESS: f"{colorama.Fore.GREEN}",
        logging.WARNING: f"{colorama.Fore.YELLOW}",
        logging.ERROR: f"{colorama.Fore.RED}",
        logging.CRITICAL: f"{colorama.Style.BRIGHT}{colorama.Fore.RED}",
    }

    RESET = colorama.Style.RESET_ALL

    def format(self, record):
        timestamp = datetime.fromtimestamp(
            record.created
        ).astimezone().isoformat(timespec="seconds", sep=" ").split("+")[0]

        color = self.COLORS.get(record.levelno, "")
        filecolor = colorama.Fore.MAGENTA

        output = (
            f"{color}"
            f"{timestamp}\t"
            f"[{record.levelname.center(8)}]    "
            f"{filecolor}"
            f"{record.filename.ljust(16 if len(record.filename) <= 16 else 22)}  "
            f"{color}"
            f"{record.threadName}: "
            f"{record.name}: "
            f"{record.getMessage()}"
            f"{self.RESET}"
        )

        if record.exc_info:
            output += (
                f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{color}{colorama.Style.NORMAL} "
                + self.formatException(record.exc_info)
                    .replace('\n', f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{color}{colorama.Style.NORMAL} ")
            )

        if record.stack_info:
            output += (
                f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{colorama.Style.RESET_ALL} "
                + self.formatStack(record.stack_info).replace('\n', f"\n {colorama.Style.DIM}#{colorama.Style.RESET_ALL} ")
            )

        return output

def getLogger(name: str) -> logging.Logger:
    if not name:
        print("???")

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(ColorFormatter())

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(handler)

    def success(message, *args, **kwargs):
        if logger.isEnabledFor(SUCCESS):
            logger._log(SUCCESS, message, args, **kwargs) # pylint: disable=protected-access

    logger.success = success
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    return logger
