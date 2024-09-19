from elasticsearch import AsyncElasticsearch
from typing_extensions import Union

from common.logger import logger
from common.exceptions import FailedToConnectErr
from common.config import settings


__all__ = (
    "els_client",
    "ElasticClient"
)


class ElasticClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """restricts creating multiple instances"""
        if cls._instance is None:
            inst = super().__new__(cls)
            cls._instance = inst
            return cls._instance
        return cls._instance

    def __init__(self, conn_addr: str):
        self._conn_addr: str = conn_addr
        self.__client: Union[AsyncElasticsearch, None] = None

    @property
    def get_client(self):
        return self.__client

    async def connect(self) -> AsyncElasticsearch:
        """creates connection to elasticsearch"""
        if self.get_client is not None:
            return self.get_client
        try:
            self.__client = AsyncElasticsearch(
                self._conn_addr
            )
            info = await self.__client.info()
            logger.info(
                msg=f"successful connection to elasticsearch: {info.body}"
            )
            return self.__client
        except Exception as e:
            logger.error(
                msg="Failed to connect to elasticsearch",
                exc_info=True
            )
            raise FailedToConnectErr(
                detail=str(e)
            )

    async def disconnect(self) -> None:
        """closes connection to elasticsearch"""
        if self.__client is not None:
            logger.info("closing elasticsearch connection")
            await self.__client.close()
            self.__client = None
        logger.warning("there is no open connection to close")


# create elastic client
els_client = ElasticClient(
    conn_addr=settings.CONNECTION_STR
)
