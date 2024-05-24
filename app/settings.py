import os

DB_USER: str = os.environ.get("db_user") or ""
DB_PORT: int = int(os.environ.get("db_port") or 5432)
DB_NAME: str = os.environ.get("db_name") or ""
DB_HOST: str = os.environ.get("db_host") or ""
DB_PASSWORD: str = os.environ.get("db_password") or ""

OPENAPI_KEY: str = os.environ.get("openapi_key") or ""

ENV: str = os.environ.get("env") or "dev"

USER_ID: int = int(os.environ.get("user_id", 2))