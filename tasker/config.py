from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    database_uri: str
    token: str = "hola"


app_settings = AppSettings()
