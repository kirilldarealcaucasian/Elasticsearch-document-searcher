import asyncio

from common.logger import logger
from internal.posts.orm_models import Base
from internal.storage import db_client


async def create_tables():
    for i in range(10):
        try:
            async with db_client._engine.begin() as con:  # create tables
                await con.run_sync(Base.metadata.drop_all)
                await con.run_sync(Base.metadata.create_all)
                logger.info(msg="tables have been created")
                break
        except Exception as e:
            logger.error(msg="failed to create tables", exc_info=str(e))
            await asyncio.sleep(8)
