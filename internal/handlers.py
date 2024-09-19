from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, Query
from pydantic import Field

from internal.elastic import els_client
from internal.elastic.elasticsearch_manager import ElasticschManager

router = APIRouter(prefix="api/v1/posts", tags=["Search"])


@router.post("/search")
async def search(
        limit: int = Query(default=20, gt=0),
        text: str = Field(min_lentgh=1),
        elastic_manager: ElasticschManager = Depends()
):
    results = await elastic_manager.search(
        elastic_client=els_client,
        text=text,
        limit=limit
    )
    return results


@router.delete("/delete/{index_id}")
async def delete(
        index_id: str | int,
        elastic_client: AsyncElasticsearch = Depends(els_client.get_client),
):
    ...

