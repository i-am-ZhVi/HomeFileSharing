from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class ConfigDataBase(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ECHO: bool = False

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

db_config = ConfigDataBase()


async_engine = create_async_engine(db_config.database_url, echo=db_config.DB_ECHO)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
