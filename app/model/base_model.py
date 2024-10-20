import json
from bson import ObjectId
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    An abstract base class for data models, providing a common interface for converting model instances to dictionaries and JSON.
    """

    @abstractmethod
    def asdict(self):
        """
        Abstract method to convert the model instance to a dictionary.

        :return: A dictionary representation of the model instance.
        :rtype: dict
        """
        pass

    def to_json(self):
        """
        Convert the model instance to a JSON string.

        This method first converts the instance to a dictionary using `asdict()`, then serializes it to JSON. Any `ObjectId` values are converted to strings to ensure proper serialization.

        :return: A JSON string representation of the model instance.
        :rtype: str
        """
        model_dict = self.asdict()
        
        for key, value in model_dict.items():
            if isinstance(value, ObjectId):
                model_dict[key] = str(value)
        
        return json.dumps(model_dict)
