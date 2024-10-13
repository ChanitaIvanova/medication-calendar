from db.mongo_db_client import MongoDBClient
from model.timesheet_model import TimeSheetModel, MedicationEntry, TimeSheetStatus
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from datetime import datetime

class Timesheets:
    COLLECTION_NAME = "timesheets"

    @staticmethod
    def __get_collection():
        collection = CollectionWrapper(Timesheets.COLLECTION_NAME)
        return collection

    @staticmethod
    def add(timesheet: TimeSheetModel):
        collection = Timesheets.__get_collection()
        result = collection.insert_one(timesheet.asdict())
        timesheet.set_id(result.inserted_id)
        print(f"Inserted timesheet with ID: {result.inserted_id}")
        return timesheet

    @staticmethod
    def find_by_user_id(user_id):
        collection = Timesheets.__get_collection()
        timesheets = list(collection.find({'user_id': user_id}))
        return [TimeSheetModel(**ts) for ts in timesheets]

    @staticmethod
    def find(id):
        collection = Timesheets.__get_collection()
        data = collection.find_by_id(id)
        return TimeSheetModel(**data) if data else None

    @staticmethod
    def delete(id):
        collection = Timesheets.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        collection = Timesheets.__get_collection()
        return [TimeSheetModel(**ts) for ts in list(collection.find())]

    @staticmethod
    def update(timesheet: TimeSheetModel):
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet.get_id())},
            {"$set": timesheet.asdict()}
        )

    @staticmethod
    def add_medication_entry(timesheet_id, medication_entry: MedicationEntry):
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$push": {"medications": medication_entry.__dict__}}
        )

    @staticmethod
    def update_status(timesheet_id, new_status: TimeSheetStatus):
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$set": {"status": new_status.value}}
        )

    @staticmethod
    def add_advise(timesheet_id, advise: str):
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$push": {"advises": advise}}
        )
