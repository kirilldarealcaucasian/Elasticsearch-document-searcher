from uuid import UUID

from sqlalchemy import select, delete

from internal.posts.schemas import PostS
from internal.storage import db_client
from typing import TypeAlias
from common.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from internal.posts.orm_models import Post

PostId: TypeAlias = str


class PostsDAO:
    """provides access to posts data"""

    async def get_posts_by_ids(self, data: list[PostId]) -> list[PostS]:
        stmt = select(Post).where(Post.id.in_(data)).order_by(Post.created_date)

        async with db_client.session as session:
            try:
                posts: list[Post] = await session.scalars(stmt)
            except SQLAlchemyError as e:
                logger.error(
                    msg="failed to retrieve posts",
                    exc_info=str(e),
                    extra={"data": data}
                )
                raise e
            return [PostS.model_validate(obj=post, from_attributes=True) for post in posts]

    async def delete_post(self, id: UUID) -> None:
        async with db_client.session as session:
            stmt = delete(Post).where(Post.id == str(id))
            await session.execute(stmt)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                logger.error(
                    msg="failed to delete post from db",
                    exc_info=str(e),
                    extra={"post_id": id}
                )
                raise e