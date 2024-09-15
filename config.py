"""Config file."""
import os

from dotenv import load_dotenv

load_dotenv()
login = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = os.getenv("POSTGRES_PORT")


def data_base_url():
    """Connect database."""
    return (f'postgresql+asyncpg://{login}:{password}@localhost:{port}'
            f'/{database}')
