import logging
import time
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

mongo = PyMongo()
logger = logging.getLogger(__name__)


def init_mongo(app):
    try:
        mongo.init_app(app)
        mongo.db.command("ping")
        print("MongoDB connected successfully")
        logging.info("MongoDB connected successfully")
    except ConnectionFailure as e:
        print("Failed to connect to Mongodb")
        logging.error(f"Mongodb connection error: {e}")
        raise e
