import json
from bson import ObjectId
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def asdict(self):
        pass

    def to_json(self):
        model_dict = self.asdict()
        
        for key, value in model_dict.items():
            if isinstance(value, ObjectId):
                model_dict[key] = str(value)
        
        return json.dumps(model_dict)