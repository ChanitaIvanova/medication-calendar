from db.mongo_db_client import MongoDBClient
from model.user_medication_model import UserMedicationModel
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from pymongo import DESCENDING, ASCENDING
import logging

class UserMedications:
    """
    A class to interact with the user_medications collection in the MongoDB database.
    """
    COLLECTION_NAME = "user_medications"

    @staticmethod
    def __get_collection():
        """
        Retrieve the collection wrapper for the user medications collection.

        :return: The collection wrapper instance for user medications.
        :rtype: CollectionWrapper
        """
        collection = CollectionWrapper(UserMedications.COLLECTION_NAME)
        return collection

    @staticmethod
    def add(user_medication: UserMedicationModel):
        """
        Add a new user medication record to the database.

        :param user_medication: The user medication model instance to add.
        :type user_medication: UserMedicationModel
        :return: The added user medication record with an updated ID.
        :rtype: UserMedicationModel
        """
        collection = UserMedications.__get_collection()
        result = collection.insert_one(user_medication.asdict())
        user_medication.set_id(result.inserted_id)
        logging.info(f"Inserted user medication record with ID: {result.inserted_id}")
        return user_medication

    @staticmethod
    def find_by_user_id(user_id, page=None, per_page=None, sort_field=None, sort_direction=None):
        """
        Find user medication records by user ID with optional pagination and sorting.

        :param user_id: The ID of the user whose medication records are to be retrieved.
        :type user_id: str
        :param page: The page number for pagination (optional).
        :type page: int, optional
        :param per_page: The number of items per page for pagination (optional).
        :type per_page: int, optional
        :param sort_field: The field by which to sort the results (optional).
        :type sort_field: str, optional
        :param sort_direction: The direction of sorting, either 'asc' or 'desc' (optional).
        :type sort_direction: str, optional
        :return: The total count of records and a list of user medication records matching the query.
        :rtype: tuple
        """
        collection = UserMedications.__get_collection()
        query = {'user_id': user_id}
        
        if page is not None and per_page is not None:
            skip = (page - 1) * per_page
            sort_params = [('_id', DESCENDING)]
            if sort_field and sort_direction:
                sort_params.insert(0, (sort_field, ASCENDING if sort_direction == 'asc' else DESCENDING))

            total_count = collection.count_documents(query)
            records = list(collection.find(query).sort(sort_params).skip(skip).limit(per_page))
            return total_count, records
        else:
            records = list(collection.find(query))
            return len(records), records

    # Add other necessary methods similar to the Medications class... 