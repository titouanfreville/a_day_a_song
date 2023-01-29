from os import environ
from uuid import uuid4

TEST_HOST = "0.0.0.0"
TEST_PORT = 8888
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"
ACCESS_TOKEN = str(uuid4())

pg_test_conf = {"user": "postgres", "password": "adasLocal*"}

DB_CONNECTION_STRING = f"postgresql://{pg_test_conf['user']}:{pg_test_conf['password']}@{environ['POSTGRES_HOST']}/{environ['POSTGRES_DB']}?sslmode=disable"
