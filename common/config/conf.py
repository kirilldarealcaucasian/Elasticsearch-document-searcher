from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal

load_dotenv()


class DataConfig(BaseModel):
    POSTS_DATA_CSV: str = "data/posts.csv"
    POSTS_DATA_JSON: str = "data/posts.json"


class Settings(BaseSettings):
    LOG_LEVEL: Literal["DEBUG", "WARNING", "INFO", "ERROR"] = "DEBUG"

    DATA_CFG: DataConfig = DataConfig()

    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_POSTS_INDEX_NAME: str

    DB_USER: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_PORT: int
    DB_NAME: str

    @property
    def ELASTIC_CONNECTION_URL(cls) -> str:  # noqa
        return f"http://{cls.ELASTIC_HOST}:{cls.ELASTIC_PORT}"

    @property
    def DB_URL(cls) -> str:  # noqa
        return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_SERVER}:{cls.DB_PORT}/{cls.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
