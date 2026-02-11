import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'hooligaps')
TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'hooligaps_test')

DB_URL = f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DB_SYNC_URL = f'postgresql+psycopg2://{DB_URL}'
DB_ASYNC_URL = f'postgresql+asyncpg://{DB_URL}'
