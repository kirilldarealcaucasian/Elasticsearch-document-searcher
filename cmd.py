import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.config import settings
from internal.elastic import els_client
from internal.handlers import router as posts_router
from internal.elastic import (
    els_manager, ElasticClient
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client: ElasticClient = await els_client.connect()  # connect to elasticsearch
    #############################################
    # if index already exists and populated with data, comment out the code below
    _ = await els_manager.create_index(
        elastic_client=client,
        index_name=settings.ELASTIC_POSTS_INDEX_NAME
    )  # create index
    await els_manager.bulk_add_data(
        elastic_client=client,
        data_path="/".join([settings.DATA_CFG, "posts.json"])
        )  # add data to index
    #############################################
    yield
    if client.get_client is not None:
        await client.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(
    router=posts_router
)


@app.get("/")
def main():
    return {
        "message": "OK"
    }


if __name__ == "__main__":
    uvicorn.run("cmd:app", reload=True)