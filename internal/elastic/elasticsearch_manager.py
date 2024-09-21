from uuid import UUID

import elasticsearch
import json

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from fastapi import Depends

from common.config import settings
from common.exceptions import AlreadyExistsErr, NotFoundErr
from common.logger import logger
from internal.posts.dao import PostsDAO


__all__ = (
    "els_manager",
    "ElasticschManager",
)

from internal.posts.schemas import PostS


class ElasticschManager:

    def __init__(self, posts_dao: PostsDAO = Depends()):
        self._posts_dao = posts_dao

    async def search(
            self,
            elastic_client: AsyncElasticsearch,
            text: str,
            limit: int
    ) -> list[PostS]:
        query = {
            "query": {
                "match": {
                    "doc.text": text
                }
            },
        }

        try:
            res = await elastic_client.search(
                index=settings.ELASTIC_POSTS_INDEX_NAME,
                body=query,
                size=limit,
            )
            response = res.body["hits"]["hits"]
        except Exception as e:
            logger.error(
                msg="failed to search",
                exc_info=str(e),
                extra={"text": text}
            )
            raise e
        post_ids: list[str] = []
        try:
            post_ids = [doc["_source"]["doc"]["id"] for doc in response]
        except Exception as e:
            logger.error(
                msg="failed to get post_ids",
                exc_info=str(e)
            )

        return await self._posts_dao.get_posts_by_ids(
            data=post_ids
        )

    async def create_index(
            self,
            elastic_client: AsyncElasticsearch,
            index_name: str
    ) -> None:
        try:
            await elastic_client.indices.create(index=settings.ELASTIC_POSTS_INDEX_NAME)
            logger.info(
                msg="elasticsearch index has been successfully created",
                extra={"index_name": index_name}
            )
        except (Exception,  elasticsearch.BadRequestError) as e:
            if type(e) == elasticsearch.BadRequestError and e.error == "resource_already_exists_exception":
                logger.debug(
                    msg="index already exists",
                    extra={"index_name": index_name}
                )
                raise AlreadyExistsErr(
                    detail=f"index {index_name} already exists"
                )
            logger.error(
                msg=f"failed to create index",
                exc_info=str(e),
                extra={"index_name": index_name}
            )

    def __gen_data(self, data_path: str):
        """creates a generator object of documents to further be used in bulk add"""
        try:
            with open(data_path, 'rt') as f:
                documents = json.loads(f.read())  # read data from json file
        except OSError as e:
            logger.error(
                msg="failed to open file",
                exc_info=str(e),
                extra={"data_path": data_path}
            )
            raise e
        for document in documents:
            to_add_document = {
                "id": document["id"],
                "text": document["text"]
            }
            yield {
                "_index": settings.ELASTIC_POSTS_INDEX_NAME,
                "doc": to_add_document
            }

    async def bulk_add_data(
            self,
            elastic_client: AsyncElasticsearch,
            data_path: str,
    ) -> None:
        try:
            await async_bulk(
                client=elastic_client,
                actions=self.__gen_data(data_path=data_path)
            )
            logger.info(msg="data has been successfully added to elasticsearch index")
        except Exception as e:
            logger.error(
                msg="failed to bulk add documents",
                exc_info=str(e),
            )

    async def delete(
            self,
            elastic_client: AsyncElasticsearch,
            post_id: UUID
    ):
        """deletes post from database and index by post id"""
        posts: list = await self._posts_dao.get_posts_by_ids([str(post_id)])

        if len(posts) == 0:
            raise NotFoundErr("post you want to delete doesn't exist")

        delete_query = {
            "match": {"doc.id": str(post_id)}
        }

        try:
            await elastic_client.delete_by_query(
                index=settings.ELASTIC_POSTS_INDEX_NAME,
                query=delete_query
            )
        except Exception as e:
            logger.error(
                msg="failed to delete document",
                exc_info=str(e),
                extra={"post_id": post_id}
            )
            raise NotFoundErr(
                detail="post wasn't found"
            )
        await self._posts_dao.delete_post(id=post_id)


els_manager = ElasticschManager()
