from db.mongo_db_client import MongoDBClient
from model.medication_model import MedicationModel
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from services.password_encoder import PasswordEncoder

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
    def find_by_user_id(user_id):
        collection = Medications.__get_collection()
        data = collection.find({"user_id": ObjectId(user_id)})
        medications = []
        for medication in data:
            medications.append(MedicationModel(**medication))
        return medications
    
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