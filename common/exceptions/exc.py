from fastapi import HTTPException, status


class FailedToConnectError(ConnectionError):
    def __init__(self, detail: str):
        self._detail = detail

    def __str__(self) -> str:
        return f"Failed to connect: {self._detail}"


class AlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "Entity already exists"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
        )


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Entity does not exist"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
        )
