import time

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

    def __init__(self, con_addr: str):
        self._conn_addr = con_addr
        self.__client: Union[AsyncElasticsearch, None] = None

    @property
    def get_client(self) -> AsyncElasticsearch:
        return self.__client

    async def connect(self) -> Union[AsyncElasticsearch, None]:
        """creates connection to elasticsearch"""
        if self.get_client is not None:
            return self.get_client
        try:
            self.__client = AsyncElasticsearch(
                self._conn_addr,
                retry_on_timeout=True,
                max_retries=3
            )
            retrials = 0
            max_retrials = 10
            while retrials <= max_retrials:
                retrials += 1
                resp = await self.__client.ping()
                if resp:
                    logger.info(msg="successful connection to elasticsearch")
                    return self.__client
                elif not resp:
                    logger.error(
                        msg="failed to connect to elasticsearch (ping failed)",
                    )
                    time.sleep(5)
                    continue
            self.__client = None
            logger.error(
                msg="connection to elasticsearch hasn't been established"
            )
            return self.__client
        except Exception as e:
            logger.error(
                msg="failed to connect to elasticsearch",
                exc_info=str(e)
            )
            if self.__client:
                await self.__client.close()
            raise FailedToConnectErr(
                        detail="failed to connect to elasticsearch"
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
    con_addr=settings.ELASTIC_CONNECTION_URL
)
