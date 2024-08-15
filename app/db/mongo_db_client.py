from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDBClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, uri="mongodb://localhost:27017/", database_name="medication_timesheet"):
        if not hasattr(self, "_initialized"):
            self._client = MongoClient(uri)
            self._database = self._client[database_name]
            self._initialized = True

    def get_database(self):
        return self._database

    def test_connection(self):
        try:
            self._client.admin.command('ping')
            print("MongoDB connection successful.")
        except ConnectionFailure:
            print("MongoDB connection failed.")