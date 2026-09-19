from typing import Literal

type StatusCode = Literal[
    "0 Success",
    "-1 Internal Error",
    "-2 Unknown error",
    "1 No Access (R)",
    "2 No Access (W)",
    "3 No Access (X)"
]

class BotError(Exception):
    def __init__(
            self,
            status_code: StatusCode,
            description: str = "",
            details: str = ""
            ):
        self.status_code: StatusCode = status_code
        self.description = description
        self.details = details

        super().__init__()

    def __str__(self):
        return f"STATUS {self.status_code} | {self.description} | {self.details}"

    def to_dc(self):
        return f"{self.description}\n-# STATUS {self.status_code}"

    def to_log(self):
        return f"STATUS {self.status_code}: {self.description}\t|\t{self.details}"

    def get_status(self):
        return f"STATUS {self.status_code}"

    def __bool__(self):
        return self.status_code != "0 Success"
