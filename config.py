from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    BINANCE_API_KEY: str
    BINANCE_SECRET_KEY: str

    BASE_URL: str


    model_config = {
        "env_file": ".env"
    }

settings = Settings() #type: ignore