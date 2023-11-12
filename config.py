import os

PG_USER = os.getenv("PG_USER", "tanny")
PG_PASSWORD = os.getenv("PG_PASSWORD", "123")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_DB = os.getenv("PG_DB", "diplomor")