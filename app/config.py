import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    dcgdb_host : str
    dcgdb_dbname : str
    dcgdb_port : str
    dcgdb_user : str
    dcgdb_pass : str

    class Config:
        env_file = ".env"


settings = Settings()