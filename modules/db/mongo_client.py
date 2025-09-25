from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()

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
            self.client = MongoClient(
                os.getenv('MONGODB_URI')
            )
            self.db = self.client[os.getenv('DB_NAME')]

        except errors.ServerSelectionTimeoutError:
            raise ConnectionError('Could not connect to MongoDB')
        except Exception as e:
            raise ConnectionError(f'Could not connect to MongoDB: {e}')

    def get_db(self):
        return self.db