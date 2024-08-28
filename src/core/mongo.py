import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from .settings import settings


class MongoContext:
    def __init__(self):
        self.uri = settings.MONGO_URL
        self.db_name = settings.MONGO_DB

    async def __aenter__(self) -> AsyncIOMotorDatabase:
        self.client = AsyncIOMotorClient(
            self.uri,
            tz_aware=True,
            uuidRepresentation="standard",
        )
        self.db = self.client.get_database(self.db_name)
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.client.close()


async def get_mongo_context():
    async with MongoContext() as db:
        yield db


async def mongo_health_check():
    try:
        async with MongoContext() as db:
            await db.command("ping")
            logging.debug("MongoDB is up and running.")
    except ConnectionFailure:
        logging.exception("MongoDB is down.")
