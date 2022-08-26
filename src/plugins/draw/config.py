from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    k_access_key: str
    k_secret_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'