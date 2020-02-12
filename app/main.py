from .core.config import PROJECT_NAME, API_STR, ALLOWED_HOSTS
from .db.mongoutils import connect_to_mongo, close_mongo_connection
from .handlers.routers import routers
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(title=PROJECT_NAME)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add events for conections database
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# add routers
app.include_router(routers, prefix=API_STR)

