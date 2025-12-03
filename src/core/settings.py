from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv()


class DatabaseSettings(BaseSettings):
    db_host: str = Field(..., alias="PGHOST")
    db_port: int = Field(..., alias="PGPORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.db_host}:"
            f"{self.db_port}/{self.postgres_db}"
        )


class AppSettings(BaseSettings):
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_dir: str = Field(..., alias="LOG_DIR")
    debug: bool = Field(False, alias="DEBUG")


class Settings:
    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


settings = Settings()

if settings.app.debug:
    import pydevd_pycharm

    pydevd_pycharm.settrace(
        host="host.docker.internal",
        port=5678,
        stdoutToServer=True,
        stderrToServer=True,
        suspend=False,
    )