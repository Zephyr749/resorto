from pymongo import MongoClient, errors
from modules.common.config import config

class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient._instance = MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise RuntimeError('MongoClient is already initialized')

        try:
            self.client = MongoClient(config.MONGODB_URI)
            self.db = self.client[config.DB_NAME]

        except errors.ServerSelectionTimeoutError:
            raise ConnectionError('Could not connect to MongoDB')
        except Exception as e:
            raise ConnectionError(f'Could not connect to MongoDB: {e}')

    def get_db(self):
        return self.db