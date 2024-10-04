"""Config file."""
import os

from dotenv import load_dotenv

load_dotenv()
login = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")
host = os.getenv("DB_HOST")


def data_base_url():
    """Connect database."""
    return (f'postgresql+asyncpg://{login}:{password}@{host}:5432/'
            f'{database}')


#Тестовое окружение
test_login = os.getenv("DB_TEST_USER")
test_password = os.getenv("DB_TEST_PASSWORD")
test_database = os.getenv("DB_TEST_NAME")
test_port = os.getenv("DB_TEST_PORT")


def data_test_base_url():
    """Connect test_database."""
    return (f'postgresql+asyncpg://{test_login}:{test_password}@localhost:{test_port}'
            f'/{test_database}')

def sync_test_base_url():
    """Connect test_database."""
    return (f'postgresql://{test_login}:{test_password}@localhost'
            f':{test_port}'
            f'/{test_database}')

# postgresql+pg8000
print(data_base_url())