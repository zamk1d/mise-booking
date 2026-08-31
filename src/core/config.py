from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "mise-booking"
    debug: bool = False
    DB_PATH: str = "./app.db"
    open_hour: int = 12
    close_hour: int = 23

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"


settings = Settings()