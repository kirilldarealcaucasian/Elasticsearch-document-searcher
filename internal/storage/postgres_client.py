from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from common.config import settings
from common.exceptions import FailedToConnectError
from common.logger import logger


class PostgresClient:
    """creates connection session to db"""

    def __init__(self, db_url: str, echo: bool):
        try:
            self._engine = create_async_engine(
                url=db_url,
                echo=echo,
            )
            logger.info("successful connection to postgres")
        except Exception as e:
            logger.error(
                "failed to connect to postgres",
                exc_info=str(e),
                extra={"db_url", db_url},
            )
            raise FailedToConnectError(detail="failed to connect to db")
        self._session = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False
        )

    @property
    def session(self) -> AsyncSession:
        return self._session()


db_client = PostgresClient(db_url=settings.DB_URL, echo=False)
