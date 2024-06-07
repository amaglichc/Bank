import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DBConfig(BaseSettings):
    url: str = os.getenv("DB_URL")


db_config = DBConfig()
