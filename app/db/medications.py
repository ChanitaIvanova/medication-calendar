from db.mongo_db_client import MongoDBClient
from model.medication_model import MedicationModel
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from services.password_encoder import PasswordEncoder
from pymongo import DESCENDING, ASCENDING
import logging

class Medications:
    """
    A class to interact with the medications collection in the MongoDB database.
    """
    COLLECTION_NAME = "medications"

    @staticmethod
    def __get_collection():
        """
        Retrieve the collection wrapper for the medications collection.

        :return: The collection wrapper instance for medications.
        :rtype: CollectionWrapper
        """
        collection = CollectionWrapper(Medications.COLLECTION_NAME)
        return collection;

    @staticmethod
    def add(medication: MedicationModel):
        """
        Add a new medication to the database.

        :param medication: The medication model instance to add.
        :type medication: MedicationModel
        :return: The added medication with an updated ID.
        :rtype: MedicationModel
        """
        collection = Medications.__get_collection()
        result = collection.insert_one(medication.asdict())
        medication.set_id(result.inserted_id)
        logging.info(f"Inserted medicine with ID: {result.inserted_id}")
        return medication

    @staticmethod
    def find_by_user_id(user_id, page=None, per_page=None, sort_field=None, sort_direction=None, filters=None):
        """
        Find medications by user ID with optional pagination, sorting, and filtering.

        :param user_id: The ID of the user whose medications are to be retrieved.
        :type user_id: str
        :param page: The page number for pagination (optional).
        :type page: int, optional
        :param per_page: The number of items per page for pagination (optional).
        :type per_page: int, optional
        :param sort_field: The field by which to sort the results (optional).
        :type sort_field: str, optional
        :param sort_direction: The direction of sorting, either 'asc' or 'desc' (optional).
        :type sort_direction: str, optional
        :param filters: A dictionary of filters to apply to the query (optional).
        :type filters: dict, optional
        :return: The total count of medications and a list of medications matching the query.
        :rtype: tuple
        """
        if page is not None and (not isinstance(page, int) or page <= 0):
            raise ValueError("Page must be a positive integer.")
        if per_page is not None and (not isinstance(per_page, int) or per_page <= 0):
            raise ValueError("Per page must be a positive integer.")

        collection = Medications.__get_collection()
        if page:
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
        else:
            query = {'user_id': user_id}
            medications = list(collection.find(query))

            return medications
        
    @staticmethod
    def count_by_user_id(user_id):
        """
        Count the number of medications for a given user.

        :param user_id: The ID of the user.
        :type user_id: str
        :return: The number of medications for the user.
        :rtype: int
        """
        collection = Medications.__get_collection()
        return collection.count_documents({'user_id': user_id})

    @staticmethod
    def find(id):
        """
        Find a medication by its ID.

        :param id: The ID of the medication to retrieve.
        :type id: str
        :return: The medication model instance if found.
        :rtype: MedicationModel
        :raises ValueError: If the medication with the given ID is not found.
        """
        collection = Medications.__get_collection()
        data = collection.find_by_id(id)
        if data is None:
            raise ValueError(f"Medication with ID {id} not found.")
        return MedicationModel(**data)
    
    @staticmethod
    def delete(id):
        """
        Delete a medication by its ID.

        :param id: The ID of the medication to delete.
        :type id: str
        :return: The result of the delete operation.
        :rtype: DeleteResult
        """
        collection = Medications.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        """
        Find all medications in the database.

        :return: A list of all medications.
        :rtype: list
        """
        collection = Medications.__get_collection()
        return list(collection.find())

    @staticmethod
    def update(medication: MedicationModel):
        """
        Update a medication in the database.

        :param medication: The medication model instance with updated data.
        :type medication: MedicationModel
        :return: The result of the update operation.
        :rtype: UpdateResult
        """
        collection = Medications.__get_collection()
        return collection.update_one(
            {"_id": ObjectId(medication.get_id())},
            {"$set": medication.asdict()}
        )

    @staticmethod
    def find_by_ids(ids):
        """
        Find medications by a list of IDs.

        :param ids: A list of medication IDs to retrieve.
        :type ids: list of str
        :return: A list of medication model instances.
        :rtype: list of MedicationModel
        :raises ValueError: If the IDs are not a list of valid ObjectId strings.
        """
        if not isinstance(ids, list) or not all(isinstance(id, str) and ObjectId.is_valid(id) for id in ids):
            raise ValueError("Ids must be a list of valid ObjectId strings.")
        
        collection = Medications.__get_collection()
        medications = list(collection.find({'_id': {'$in': [ObjectId(id) for id in ids]}}))
        return [MedicationModel(**med) for med in medications]
