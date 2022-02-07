import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    p2eguildadm_host : str
    p2eguildadm_dbname : str
    p2eguildadm_port : str
    p2eguildadm_user : str
    p2eguildadm_pass : str

    class Config:
        env_file = ".env"


settings = Settings()