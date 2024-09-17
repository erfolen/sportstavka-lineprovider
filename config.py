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


#Тестовое окружение
test_login = os.getenv("TEST_POSTGRES_USER")
test_password = os.getenv("TEST_POSTGRES_PASSWORD")
test_database = os.getenv("TEST_POSTGRES_DB")
test_port = os.getenv("TEST_POSTGRES_PORT")


def data_test_base_url():
    """Connect test_database."""
    return (f'postgresql+asyncpg://{test_login}:{test_password}@localhost:{test_port}'
            f'/{test_database}')
