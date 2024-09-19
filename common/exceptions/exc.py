

class FailedToConnectErr(Exception):
    def __init__(self, detail: str):
        self._detail = detail

    def __str__(self) -> str:
        return f"Failed to connect: {self._detail}"
