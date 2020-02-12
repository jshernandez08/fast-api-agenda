import logging
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_to_mongo():
    logging.info("Conecting to database...")
    db.client = AsyncIOMotorClient(
        str(MONGODB_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT
    )
    logging.info("Conection successfull!")


async def close_mongo_connection():
    logging.info("Close conection with databse...")
    db.client.close()
    logging.info("Conection close successfull！")
