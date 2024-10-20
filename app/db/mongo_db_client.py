from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import threading
import logging
import configparser
import time

class MongoDBClient:
    """
    A thread-safe singleton class to manage MongoDB connections.
    """
    _instance = None
    _lock = threading.Lock()
    _config = None
    DATABASE_CONFIG_KEY = 'Database'

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of MongoDBClient if it does not exist, ensuring thread safety.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MongoDBClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, config_path='config.dev.ini'):
        """
        Initialize the MongoDBClient by loading the configuration and establishing a database connection.

        :param config_path: Path to the configuration file.
        :type config_path: str
        :raises ValueError: If the required database configuration is missing.
        :raises ConnectionFailure: If the connection to MongoDB fails after multiple attempts.
        """
        if MongoDBClient._config is None:
            MongoDBClient._config = self._load_config(config_path)
        if MongoDBClient.DATABASE_CONFIG_KEY not in MongoDBClient._config or 'uri' not in MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY] or 'name' not in MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY]:
            raise ValueError("Missing required database configuration. Please ensure 'Database', 'uri', and 'name' are set in the configuration file.")
        uri = MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY]['uri']
        database_name = MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY]['name']
        max_pool_size = int(MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY].get('maxPoolSize', 50))
        min_pool_size = int(MongoDBClient._config[MongoDBClient.DATABASE_CONFIG_KEY].get('minPoolSize', 10))
        if not self.is_initialized():
            retries = 3
            for attempt in range(retries):
                try:
                    self._client = MongoClient(uri, maxPoolSize=max_pool_size, minPoolSize=min_pool_size)
                    self._database = self._client[database_name]
                    self._initialized = True
                    break
                except ConnectionFailure as e:
                    logging.error(f"Attempt {attempt + 1} to connect to MongoDB failed. Error: {e}")
                    if attempt < retries - 1:
                        time.sleep(5)  # Wait for 5 seconds before retrying
                    else:
                        raise ConnectionFailure("Failed to connect to MongoDB after multiple attempts.")

    def is_initialized(self):
        """
        Check if the MongoDB client has been initialized.

        :return: True if the client is initialized, False otherwise.
        :rtype: bool
        """
        return getattr(self, "_initialized", False)

    def get_database(self):
        """
        Get the MongoDB database instance.

        :return: The MongoDB database instance.
        :rtype: Database
        :raises ConnectionFailure: If the MongoDB client is not initialized.
        """
        if not self.is_initialized():
            raise ConnectionFailure("MongoDB client is not initialized.")
        return self._database

    def test_connection(self):
        """
        Test the connection to the MongoDB server.

        Logs a success message if the connection is successful, otherwise logs an error.
        """
        try:
            self._client.admin.command('ping')
            logging.info("MongoDB connection successful.")
        except ConnectionFailure as e:
            logging.error(f"MongoDB connection failed. Error: {e}")
            
    def _load_config(self, config_path):
        """
        Load the configuration file.

        :param config_path: Path to the configuration file.
        :type config_path: str
        :return: The loaded configuration object.
        :rtype: ConfigParser
        :raises FileNotFoundError: If the configuration file is not found or is empty.
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.sections():
            raise FileNotFoundError(f"Configuration file '{config_path}' not found or is empty.")
        return config
