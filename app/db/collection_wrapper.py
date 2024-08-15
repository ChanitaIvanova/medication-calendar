from db.mongo_db_client import MongoDBClient
from model.user import User
from bson.objectid import ObjectId

class CollectionWrapper:
    def __init__(self, collection_name):
        mongo_client = MongoDBClient()
        db = mongo_client.get_database()
        self.collection = db[collection_name]

    
    def find_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update_by_id(self, id, item):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": item})
    
    def __getattr__(self, name):
        return getattr(self.collection, name)