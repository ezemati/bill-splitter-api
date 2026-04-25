from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 5
    refresh_token_expire_minutes: int = 60 * 24 * 7


class DbSettings(BaseModel):
    user: str
    password: str
    name: str
    host: str
    port: int

    def get_sqlalchemy_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    jwt: JwtSettings
    db: DbSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=[".env", ".env.local", ".env.production"],
        env_file_encoding="utf-8",
        nested_model_default_partial_update=True,
    )


settings = Settings()  # type: ignore
