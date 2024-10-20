from db.mongo_db_client import MongoDBClient
from bson.objectid import ObjectId

class CollectionWrapper:
    """
    A wrapper class for a MongoDB collection to provide additional functionality and ease of use.
    """
    def __init__(self, collection_name, mongo_client=None):
        """
        Initialize the CollectionWrapper instance.

        :param collection_name: The name of the collection to interact with.
        :type collection_name: str
        :param mongo_client: An optional MongoDB client instance. If not provided, a new client will be created.
        :type mongo_client: MongoDBClient, optional
        """
        if mongo_client is None:
            mongo_client = MongoDBClient()
        db = mongo_client.get_database()
        self.collection = db[collection_name]

    def find_by_id(self, id):
        """
        Find a document in the collection by its ID.

        :param id: The ID of the document to retrieve.
        :type id: str
        :return: The document if found, otherwise None.
        :rtype: dict or None
        :raises ValueError: If the provided ID is not a valid ObjectId format.
        """
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid ObjectId format.")
        return self.collection.find_one({"_id": ObjectId(id)})

    def update_by_id(self, id, item):
        """
        Update a document in the collection by its ID.

        :param id: The ID of the document to update.
        :type id: str
        :param item: The fields to update in the document.
        :type item: dict
        :raises ValueError: If the provided ID is not a valid ObjectId format or if the document is not found.
        """
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid ObjectId format.")
        result = self.collection.update_one({"_id": ObjectId(id)}, {"$set": item})
        if result.matched_count == 0:
            raise ValueError(f"Document with ID {id} not found.")
    
    def __getattr__(self, name):
        """
        Delegate attribute access to the underlying MongoDB collection.

        :param name: The name of the attribute or method to access.
        :type name: str
        :return: The attribute or method of the underlying collection.
        """
        return getattr(self.collection, name)
