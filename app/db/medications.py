from db.mongo_db_client import MongoDBClient
from model.medication_model import MedicationModel
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from services.password_encoder import PasswordEncoder
from pymongo import DESCENDING, ASCENDING

class Medications:
    COLLECTION_NAME = "medications"

    @staticmethod
    def __get_collection():
        collection = CollectionWrapper(Medications.COLLECTION_NAME)
        return collection;

    @staticmethod
    def add(medication: MedicationModel):
        collection = Medications.__get_collection()
        result = collection.insert_one(medication.asdict())
        medication.set_id(result.inserted_id)
        print(f"Inserted medicine with ID: {result.inserted_id}")
        return medication

    @staticmethod
    def find_by_user_id(user_id, page, per_page, sort_field=None, sort_direction=None, filters=None):
        collection = Medications.__get_collection()
        skip = (page - 1) * per_page

        query = {'user_id': user_id}
        if filters:
            for field, value in filters.items():
                if value:
                    query[field] = {'$regex': value, '$options': 'i'}

        sort_params = [('_id', DESCENDING)]
        if sort_field and sort_direction:
            sort_params.insert(0, (sort_field, ASCENDING if sort_direction == 'asc' else DESCENDING))

        total_count = collection.count_documents(query)
        medications = list(collection.find(query).sort(sort_params).skip(skip).limit(per_page))

        return total_count, medications

    @staticmethod
    def count_by_user_id(user_id):
        collection = Medications.__get_collection()
        return collection.count_documents({'user_id': user_id})

    @staticmethod
    def find(id):
        collection = Medications.__get_collection()
        data = collection.find_by_id(id)
        return MedicationModel(**data)
    
    @staticmethod
    def delete(id):
        collection = Medications.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        collection = Medications.__get_collection()
        return list(collection.find())

    @staticmethod
    def update(medication: MedicationModel):
        collection = Medications.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(medication.get_id())},
            {"$set": medication.asdict()}
        )