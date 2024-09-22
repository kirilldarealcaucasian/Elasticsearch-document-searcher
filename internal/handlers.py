from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status

from internal.elastic import els_client
from internal.elastic.elasticsearch_manager import ElasticschManager
from internal.posts.schemas import PostS

router = APIRouter(prefix="/api/v1/posts", tags=["Search"])


@router.post(
    "/search", response_model=list[PostS], status_code=status.HTTP_200_OK
)
async def search(
    limit: int = Query(default=20, gt=0),
    text: str = Body(min_length=1, media_type="text/plain"),
    elastic_manager: ElasticschManager = Depends(),
):
    results = await elastic_manager.search(
        elastic_client=els_client.get_client, text=text, limit=limit
    )
    return results


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    post_id: UUID, elastic_manager: ElasticschManager = Depends()
) -> None:
    await elastic_manager.delete(
        post_id=post_id, elastic_client=els_client.get_client
    )
