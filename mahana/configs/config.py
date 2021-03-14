import os
import pathlib

from dataclasses import dataclass


@dataclass
class AppConfig:
    APP_PATH: pathlib = pathlib.Path(os.path.realpath(__file__)).parent.parent

    WEB_PORT: int = 7679
    WEB_HOST: str = "0.0.0.0"


@dataclass
class DatabaseConfig:
    BASE_DB: str = "mahana"

    DB_PORT: int = 27017
    DB_HOST: str = "127.0.0.1"

    CONNECT_URI:str = f"mongodb://{DB_HOST}:{DB_PORT}"
