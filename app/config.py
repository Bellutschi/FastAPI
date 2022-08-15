from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    database_port: str = Field(..., env="DATABASE_PORT")
    database_password: SecretStr = Field(..., env="DATABASE_PASSWORD")
    database_name: str = Field(..., env="DATABASE_NAME")
    database_username: str = Field(..., env="DATABASE_USERNAME")
    database_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    secret_key:  str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    acces_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"

settings = Settings()