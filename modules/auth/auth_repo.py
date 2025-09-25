from modules.db.mongo_client import MongoDBClient
from modules.db.schemas import UserCreate


class AuthRepository:
    def __init__(self):
        self.db = MongoDBClient.get_instance().get_db()

    def getUserByEmail(self, email:str):
        return self.db.users.find_one({"email":email})

    def insertUser(self, user:UserCreate):
        return self.db.users.insert_one(dict(user))