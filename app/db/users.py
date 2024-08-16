from db.mongo_db_client import MongoDBClient
from model.user import User
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from services.password_encoder import PasswordEncoder

class Users:
    COLLECTION_NAME = "users"

    @staticmethod
    def __get_collection():
        collection = CollectionWrapper(Users.COLLECTION_NAME)
        return collection;

    @staticmethod
    def add(user: User):
        collection = Users.__get_collection()
        user.password = PasswordEncoder.encode_password(user.password)
        result = collection.insert_one(user.asdict())
        user.set_id(result.inserted_id)
        print(f"Inserted user with ID: {result.inserted_id}")
        return user

    @staticmethod
    def find(id):
        collection = Users.__get_collection()
        data = collection.find_by_id(id)
        return User(**data)
        
    @staticmethod
    def update_useremail(id, email):
        collection = Users.__get_collection()
        data = collection.find_by_id(id)
        user = User(**data)
        print(f"Found user: {user}")
        user.email = email
        collection.update_by_id(id, user.asdict())
        print(f"Updated user: {user}")
        return user
    
    @staticmethod
    def delete(id):
        collection = Users.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        collection = Users.__get_collection()
        return list(collection.find())
    
    @staticmethod
    def find_by_username(username):
        collection = Users.__get_collection()
        user = collection.find_one({"username": username})
        if user:
            return User(**user)
        return None

    @staticmethod
    def find_by_email(email):
        collection = Users.__get_collection()
        user = collection.find_one({"email": email})
        if user:
            return User(**user)
        return None

    @staticmethod
    def find_existing_user(email, username):
        collection = Users.__get_collection()
        existing_user = collection.find_one({
            "$or": [
                {"email": email},
                {"username": username}
            ]
        })
        return existing_user