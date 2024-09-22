from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.config import settings
from common.exceptions import AlreadyExistsError
from common.logger import logger
from internal.elastic import els_client, els_manager
from internal.handlers import router as posts_router
from internal.utils import create_tables, populate_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """performs set-up logic before application has been started"""
    els_con: AsyncElasticsearch = (
        await els_client.connect()
    )  # connect to elasticsearch
    await create_tables()
    await populate_db(path=settings.DATA_CFG.POSTS_DATA_JSON)  # inserts data
    if els_con:
        try:
            _ = await els_manager.create_index(
                elastic_client=els_con,
                index_name=settings.ELASTIC_POSTS_INDEX_NAME,
            )  # create index
        except AlreadyExistsError:
            pass
        await els_manager.bulk_add_data(
            elastic_client=els_con, data_path=settings.DATA_CFG.POSTS_DATA_JSON
        )  # add data to index
    yield
    if els_con:
        await els_con.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router=posts_router)


app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_errors(request: Request, call_next):
    """multiplexes unprocessed errors into error with status code 500"""
    try:
        response = await call_next(request)
    except Exception as e:
        if not isinstance(e, HTTPException):
            logger.error(
                msg="something went wrong",
                exc_info=str(e),
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "something went wrong"},
            )
        raise e
    return response


@app.get("/")
async def main():
    client = els_client.get_client
    res = await client.info()
    return res


if __name__ == "__main__":
    uvicorn.run("cmd:app", reload=True)
