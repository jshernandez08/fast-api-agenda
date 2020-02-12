import os
from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_STR = "/api/v1"
JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 0))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 0))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", ""))

PROJECT_NAME = os.getenv("PROJECT_NAME", "")

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

DEBUG_MODE = bool(os.getenv("DEBUG_MODE", True))
MONGO_DB = os.getenv("MONGO_DB", "")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

if not DEBUG_MODE:
    MONGO_USER = os.getenv("MONGO_USER", "")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "")
    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )
else:
    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )

database_name = MONGO_DB
contacts_collection_name = "contacts"