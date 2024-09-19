from elasticsearch import AsyncElasticsearch
from pydantic import json
from common.config import settings

__all__ = (
    "els_manager",
    "ElasticschManager"
)


class ElasticschManager:

    async def search(
            self,
            elastic_client: AsyncElasticsearch,
            text: str,
            limit: int
    ):
        results = await elastic_client.search(
            index=settings.ELASTIC_POSTS_INDEX_NAME,
            body={
                "match": {
                    "text": {
                        "query": text
                    }
                }
            },
            size=limit,
            sort=["created_date"]
        )
        return results

    async def create_index(
            self,
            elastic_client: AsyncElasticsearch,
            index_name: str
    ):
        await elastic_client.indices.delete(
            index=index_name,
            ignore_unavailable=True
        )
        await elastic_client.indices.create(index=settings.ELASTIC_POSTS_INDEX_NAME)

    async def bulk_add_data(
            self,
            elastic_client: AsyncElasticsearch,
            data_path: str,
    ):
        with open(data_path, 'rt') as f:
            documents = json.loads(f.read())

        operations = []
        print("OPERATIONS: ", operations)

        for document in documents:
            operations.append({'index': {'_index': settings.ELASTIC_POSTS_INDEX_NAME}})
            operations.append(document)
        return await elastic_client.bulk(operations=operations)


els_manager = ElasticschManager()

