import json
from internal.storage import db_client
from sqlalchemy import insert
from internal.posts.orm_models import Post
from datetime import datetime
from common.logger import logger
from sqlalchemy.exc import SQLAlchemyError


__all__ = (
    "populate_db",
)


def object_hook(obj: dict):
    """
    converts string representation of list to list
    of strings and datetime string to datetime object
    """
    obj = obj.copy()
    rubrics: str = obj.get("rubrics")
    fixed_rubrics = rubrics.replace("'", '"')  # json requires double quotes for string literals
    deserialized_rubrics = json.loads(
        fixed_rubrics
    )  # conversion
    obj["rubrics"] = deserialized_rubrics
    obj["created_date"] = datetime.strptime(
        obj["created_date"],
        "%d.%m.%Y %H:%M"
    )  # convert from string representation to datetime object
    return obj


async def populate_db(path):
    """populates db from json data"""
    try:
        with open(path, "rt", encoding="utf-8") as f:
            data = json.load(f, object_hook=object_hook)
    except (OSError, Exception, FileNotFoundError) as e:
        if type(e) == OSError:
            logger.error(
                msg="failed to open the file",
                exc_info=str(e),
                extra={"file_path": path}
            )
            return
        elif type(e) == FileNotFoundError:
            logger.error(
                msg="failed to populate db: file wasn't found (check correctness of file path)",
                exc_info=str(e),
                extra={"file_path": path}
            )
            return
        else:
            logger.error(
                msg="failed to deserialize file"
            )
            return

    async with db_client.session as session:
        stmt = insert(Post).values(data)
        try:
            await session.execute(stmt)
            await session.commit()
            logger.info("database has been successfully populated with data")
        except SQLAlchemyError as e:
            logger.error("failed to commit session")
            raise e
