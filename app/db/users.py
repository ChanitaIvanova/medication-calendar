from db.mongo_db_client import MongoDBClient
from model.user_model import UserModel
from db.collection_wrapper import CollectionWrapper
from bson.objectid import ObjectId
from services.password_encoder import PasswordEncoder
import logging
import re

class Users:
    """
    A class to interact with the users collection in the MongoDB database.
    """
    COLLECTION_NAME = "users"

    @staticmethod
    def __get_collection():
        """
        Retrieve the collection wrapper for the users collection.

        :return: The collection wrapper instance for users.
        :rtype: CollectionWrapper
        """
        collection = CollectionWrapper(Users.COLLECTION_NAME)
        return collection;

    @staticmethod
    def add(user: UserModel):
        """
        Add a new user to the database.

        :param user: The user model instance to add.
        :type user: UserModel
        :return: The added user with an updated ID.
        :rtype: UserModel
        """
        collection = Users.__get_collection()
        user.password = PasswordEncoder.encode_password(user.password)
        result = collection.insert_one(user.asdict())
        user.set_id(result.inserted_id)
        logging.info(f"Inserted user with ID: {result.inserted_id}")
        return user

    @staticmethod
    def find(id):
        """
        Find a user by its ID.

        :param id: The ID of the user to retrieve.
        :type id: str
        :return: The user model instance if found.
        :rtype: UserModel
        :raises ValueError: If the user with the given ID is not found.
        """
        collection = Users.__get_collection()
        data = collection.find_by_id(id)
        if data is None:
            raise ValueError(f"User with ID {id} not found.")
        return UserModel(**data)
        
    @staticmethod
    def update_useremail(id, email):
        """
        Update the email address of a user.

        :param id: The ID of the user to update.
        :type id: str
        :param email: The new email address to set.
        :type email: str
        :return: The updated user model instance.
        :rtype: UserModel
        :raises ValueError: If the user ID or email format is invalid, or if the user is not found.
        """
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid user ID format.")
        if not isinstance(email, str) or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            raise ValueError("Invalid email format.")
        
        collection = Users.__get_collection()
        data = collection.find_by_id(id)
        if data is None:
            raise ValueError(f"User with ID {id} not found.")
        user = UserModel(**data)
        print(f"Found user: {user}")
        user.email = email
        collection.update_by_id(id, user.asdict())
        print(f"Updated user: {user}")
        return user
    
    @staticmethod
    def delete(id):
        """
        Delete a user by its ID.

        :param id: The ID of the user to delete.
        :type id: str
        :return: The result of the delete operation.
        :rtype: DeleteResult
        :raises ValueError: If the user ID format is invalid.
        """
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid user ID format.")
        
        collection = Users.__get_collection()
        return collection.delete_one({"_id": ObjectId(id)})

    @staticmethod
    def findAll():
        """
        Find all users in the database.

        :return: A list of all user model instances.
        :rtype: list of UserModel
        """
        collection = Users.__get_collection()
        return list(collection.find())
    
    @staticmethod
    def find_by_username(username):
        """
        Find a user by their username.

        :param username: The username of the user to retrieve.
        :type username: str
        :return: The user model instance if found, otherwise None.
        :rtype: UserModel or None
        """
        collection = Users.__get_collection()
        user = collection.find_one({"username": username})
        if user:
            return UserModel(**user)
        return None

    @staticmethod
    def find_by_email(email):
        """
        Find a user by their email address.

        :param email: The email address of the user to retrieve.
        :type email: str
        :return: The user model instance if found, otherwise None.
        :rtype: UserModel or None
        """
        collection = Users.__get_collection()
        user = collection.find_one({"email": email})
        if user:
            return UserModel(**user)
        return None

    @staticmethod
    def find_existing_user(email, username):
        """
        Find an existing user by their email or username.

        :param email: The email address to search for.
        :type email: str
        :param username: The username to search for.
        :type username: str
        :return: The existing user if found, otherwise None.
        :rtype: dict or None
        """
        collection = Users.__get_collection()
        # Ensure indexes exist for email and username fields to optimize query performance
        collection.create_index("email", unique=True)
        collection.create_index("username", unique=True)
        existing_user = collection.find_one({
            "$or": [
                {"email": email},
                {"username": username}
            ]
        })
        return existing_user
