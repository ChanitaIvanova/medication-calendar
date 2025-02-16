from dataclasses import dataclass, asdict
from flask_login import UserMixin
from .roles import Role
from .base_model import BaseModel  # Import the BaseModel
import logging

@dataclass
class UserModel(UserMixin, BaseModel):  # Inherit from BaseModel
    """
    A data model representing a user.

    Attributes:
        _id (str): The unique identifier of the user.
        id (str): A redundant identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        role (Role): The role of the user, defining their permissions.
    """
    _id: str
    id: str
    username: str
    email: str
    password: str
    role: Role

    def __init__(self, username: str, email: str, password: str, role = Role.USER, _id = -1):
        """
        Initialize a new UserModel instance.

        :param username: The username of the user.
        :type username: str
        :param email: The email address of the user.
        :type email: str
        :param password: The hashed password of the user.
        :type password: str
        :param role: The role of the user, default is Role.USER. Can be Role enum or string.
        :type role: Role or str
        :param _id: The unique identifier of the user, default is -1.
        :type _id: int or str
        """
        self._id = _id
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
        # Convert string role to Role enum if necessary
        self.role = Role(role) if isinstance(role, str) else role

    def set_id(self, id):
        """
        Set the unique identifier for the user.

        :param id: The unique identifier to set.
        :type id: int or str
        """
        self._id = id
        
    def get_id(self):
        """
        Get the unique identifier of the user.

        :return: The unique identifier of the user.
        :rtype: str
        """
        return str(self._id)

    def asdict(self):
        """
        Convert the UserModel instance to a dictionary.

        :return: A dictionary representation of the user.
        :rtype: dict
        """
        dictionary = asdict(self)
        dictionary.pop('_id', None)
        dictionary.pop('id', None)
        dictionary['role'] = self.role.value
        return dictionary
    
    def has_role(self, role: Role):
        """
        Check if the user has the specified role.

        :param role: The role to check against.
        :type role: Role
        :return: True if the user has the specified role, False otherwise.
        :rtype: bool
        """
        return self.role == role

    def log(self):
        """
        Log the details of the user using the logging module.
        """
        logging.info(f"User: {self.username}, {self.email}, {self.password}, {self._id}, {self.role}")
