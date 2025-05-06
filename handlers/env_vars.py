import os


class EnvVars:
    DB_URL = os.getenv("DATABASE_URL")
