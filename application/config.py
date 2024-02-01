import os
import sys


def get_test_db_name(db_name: str) -> str:
    worker_id = os.getenv("PYTEST_XDIST_WORKER")
    if worker_id is None:
        worker_id = "gw0"
    return f"test_{db_name}_{worker_id}"


def create_connection_url(
    db_user: str,
    db_host: str,
    db_port: str,
    db_password: str,
    db_database: str,
) -> str:
    return (
        f"postgresql+asyncpg://"
        f"{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    )


POSTGRESQL_USER = os.getenv("POSTGRESQL_USER", "postgres")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST", "127.0.0.1")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT", "5432")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "postgres")
POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE", "trade_hub")

IS_PYTEST = "pytest" in sys.argv[0] or "PYTEST_XDIST_WORKER" in os.environ
IS_DEBUG: bool = os.getenv("IS_DEBUG", "True") == "True"

if IS_PYTEST:
    POSTGRESQL_DATABASE = get_test_db_name(POSTGRESQL_DATABASE)

POSTGRESQL_URL = create_connection_url(
    db_user=POSTGRESQL_USER,
    db_host=POSTGRESQL_HOST,
    db_port=POSTGRESQL_PORT,
    db_password=POSTGRESQL_PASSWORD,
    db_database=POSTGRESQL_DATABASE,
)
