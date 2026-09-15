from typing import Literal

class BotError(Exception):
    def __init__(
            self,
            status_code: Literal[
                "0 Success",
                "-1 Internal Error",
                "-2 Unknown error",
                "1 No Access (W)"
            ],
            description: str = "",
            details: str = ""
            ):
        self.status_code = status_code
        self.description = description
        self.details = details

    def __str__(self):
        return f"STATUS {self.status_code}\n{self.description}\n{self.details}"

    def to_dc(self):
        return f"{self.description}\n-# STATUS {self.status_code}"

    def to_log(self):
        return f"STATUS {self.status_code}: {self.description}\t|\t{self.details}"
