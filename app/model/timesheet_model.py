from dataclasses import dataclass, asdict, field
from datetime import date
from enum import Enum
from typing import List
from .base_model import BaseModel
from datetime import datetime


class TimeSheetStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

@dataclass
class MedicationEntry:
    id: str
    dosage: str
    advise: str
    dates: List[str]
    name: str = ""  # Add this line to include the name of the medication

@dataclass
class TimeSheetModel(BaseModel):
    id: str
    user_id: str
    medications: List[MedicationEntry]
    status: TimeSheetStatus
    start_date: str
    end_date: str

    def __init__(
        self,
        user_id: str,
        medications: List[MedicationEntry],
        status: TimeSheetStatus,
        start_date: str,
        end_date: str,
        _id=-1,
        id=-1
    ):
        self._id = _id
        self.id = _id
        self.user_id = user_id
        self.medications = []
        for med in medications:
            if isinstance(med, MedicationEntry): 
                self.medications.append(med) 
            else: self.medications.append(MedicationEntry(**med)) 
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return str(self._id)

    def asdict(self):
        dictionary = asdict(self)
        dictionary.update({'id': str(self._id)})
        dictionary['status'] = self.status
        dictionary['medications'] = [asdict(med) for med in self.medications]
        return dictionary

    def print(self):
        print(f"TimeSheet: User ID: {self.user_id}, Status: {self.status.value}")
        for med in self.medications:
            print(f"  Medication: {med.id}, Dosage: {med.dosage}, Dates: {med.dates}")
        print(f"Advise: {self.advise}")
