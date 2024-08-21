from dataclasses import dataclass, asdict
from flask_login import UserMixin
from .roles import Role

@dataclass
class UserModel(UserMixin):
    _id: str
    id: str
    username: str
    email: str
    password: str
    role: Role

    def __init__(self, username: str, email: str, password: str, role = Role.USER, _id = -1):
        self._id = _id
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def set_id(self, id):
        self._id = id
        
    def get_id(self):
        return str(self._id)

    def asdict(self):
        dictionary = asdict(self)
        dictionary.pop('_id', None)
        dictionary.pop('id', None)
        dictionary['role'] = self.role.value
        print(dictionary)
        return dictionary
    
    def has_role(self, role: Role):
        return self.role == role

    def print(self):
        print(f"User: {self.username}, {self.email}, {self.password}, {self._id}, {self.role}")
