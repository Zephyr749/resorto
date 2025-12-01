from modules.db.mongo_client import MongoDBClient
from modules.db.schemas import UserCreate, DBUser
from bson import ObjectId


class AuthRepository:
    def __init__(self):
        self.db = MongoDBClient.get_instance().get_db()

    def getUserByEmail(self, email: str) -> DBUser | None:
        return self.db.users.find_one({'email': email})

    def getUserById(self, userId: str) -> DBUser | None:
        return self.db.users.find_one({'_id': ObjectId(userId)})

    def insertUser(self, user: UserCreate):
        return self.db.users.insert_one(dict(user))

    def updateUser(self, userId: str, firstName: str, lastName: str):
        return self.db.users.update_one(
            {'_id': ObjectId(userId)},
            {'$set': {'firstName': firstName, 'lastName': lastName}}
        )

    def updatePassword(self, userId: str, hashedPassword: str):
        return self.db.users.update_one(
            {'_id': ObjectId(userId)},
            {'$set': {'password': hashedPassword}}
        )