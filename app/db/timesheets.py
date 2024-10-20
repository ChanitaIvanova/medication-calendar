from db.mongo_db_client import MongoDBClient
from model.timesheet_model import TimeSheetModel, MedicationEntry, TimeSheetStatus
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from datetime import datetime
import logging

class Timesheets:
    """
    A class to interact with the timesheets collection in the MongoDB database.
    """
    COLLECTION_NAME = "timesheets"

    @staticmethod
    def __get_collection():
        """
        Retrieve the collection wrapper for the timesheets collection.

        :return: The collection wrapper instance for timesheets.
        :rtype: CollectionWrapper
        """
        collection = CollectionWrapper(Timesheets.COLLECTION_NAME)
        return collection

    @staticmethod
    def add(timesheet: TimeSheetModel):
        """
        Add a new timesheet to the database.

        :param timesheet: The timesheet model instance to add.
        :type timesheet: TimeSheetModel
        :return: The added timesheet with an updated ID.
        :rtype: TimeSheetModel
        """
        collection = Timesheets.__get_collection()
        result = collection.insert_one(timesheet.asdict())
        timesheet.set_id(result.inserted_id)
        logging.info(f"Inserted timesheet with ID: {result.inserted_id}")
        return timesheet

    @staticmethod
    def find_by_user_id(user_id):
        """
        Find timesheets by user ID.

        :param user_id: The ID of the user whose timesheets are to be retrieved.
        :type user_id: str
        :return: A list of timesheet model instances matching the user ID.
        :rtype: list of TimeSheetModel
        :raises ValueError: If the user ID is not a valid format.
        """
        if not isinstance(user_id, str) or not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID format.")
        
        collection = Timesheets.__get_collection()
        timesheets = list(collection.find({'user_id': user_id}))
        return [TimeSheetModel(**ts) for ts in timesheets]

    @staticmethod
    def find(id):
        """
        Find a timesheet by its ID.

        :param id: The ID of the timesheet to retrieve.
        :type id: str
        :return: The timesheet model instance if found.
        :rtype: TimeSheetModel
        :raises ValueError: If the timesheet with the given ID is not found.
        """
        collection = Timesheets.__get_collection()
        data = collection.find_by_id(id)
        if data is None:
            raise ValueError(f"Timesheet with ID {id} not found.")
        return TimeSheetModel(**data)

    @staticmethod
    def delete(id):
        """
        Delete a timesheet by its ID.

        :param id: The ID of the timesheet to delete.
        :type id: str
        :return: The result of the delete operation.
        :rtype: DeleteResult
        :raises ValueError: If the timesheet ID is not a valid format.
        """
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid timesheet ID format.")
        
        collection = Timesheets.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        """
        Find all timesheets in the database.

        :return: A list of all timesheet model instances.
        :rtype: list of TimeSheetModel
        """
        collection = Timesheets.__get_collection()
        return [TimeSheetModel(**ts) for ts in list(collection.find())]

    @staticmethod
    def update(timesheet: TimeSheetModel):
        """
        Update a timesheet in the database.

        :param timesheet: The timesheet model instance with updated data.
        :type timesheet: TimeSheetModel
        :return: The result of the update operation.
        :rtype: UpdateResult
        """
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet.get_id())},
            {"$set": timesheet.asdict()}
        )

    @staticmethod
    def add_medication_entry(timesheet_id, medication_entry: MedicationEntry):
        """
        Add a medication entry to a timesheet.

        :param timesheet_id: The ID of the timesheet to update.
        :type timesheet_id: str
        :param medication_entry: The medication entry to add.
        :type medication_entry: MedicationEntry
        :return: The result of the update operation.
        :rtype: UpdateResult
        """
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$push": {"medications": medication_entry.__dict__}}
        )

    @staticmethod
    def update_status(timesheet_id, new_status: TimeSheetStatus):
        """
        Update the status of a timesheet.

        :param timesheet_id: The ID of the timesheet to update.
        :type timesheet_id: str
        :param new_status: The new status to set for the timesheet.
        :type new_status: TimeSheetStatus
        :return: The result of the update operation.
        :rtype: UpdateResult
        """
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$set": {"status": new_status.value}}
        )

    @staticmethod
    def add_advise(timesheet_id, advise: str):
        """
        Add an advise entry to a timesheet.

        :param timesheet_id: The ID of the timesheet to update.
        :type timesheet_id: str
        :param advise: The advise text to add.
        :type advise: str
        :return: The result of the update operation.
        :rtype: UpdateResult
        """
        collection = Timesheets.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(timesheet_id)},
            {"$push": {"advises": advise}}
        )
