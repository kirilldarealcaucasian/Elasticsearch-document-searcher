from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal

load_dotenv()


class DataConfig(BaseModel):
    DATA_PATH: str = "project/data"


class Settings(BaseSettings):
    LOG_LEVEL: Literal["DEBUG", "WARNING", "INFO", "ERROR"]
    DATA_CFG: DataConfig = DataConfig()
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_POSTS_INDEX_NAME: str

    @property
    def CONNECTION_STR(cls) -> str:  # noqa
        return f"http://{cls.ELASTIC_HOST}:{cls.ELASTIC_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()




