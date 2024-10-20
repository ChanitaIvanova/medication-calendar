from dataclasses import dataclass, asdict
from enum import Enum
from typing import List
from .base_model import BaseModel
import logging

class TimeSheetStatus(Enum):
    """
    Enumeration representing the status of a timesheet.

    Attributes:
        ACTIVE: Timesheet is currently active.
        INACTIVE: Timesheet is not active.
        EXPIRED: Timesheet has expired.
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

@dataclass
class MedicationEntry:
    """
    A data model representing an entry for a medication in a timesheet.

    Attributes:
        id (str): The unique identifier of the medication.
        dosage (str): The dosage information for the medication.
        advise (str): The medical advice associated with the medication.
        dates (List[str]): List of dates when the medication should be taken.
        name (str): The name of the medication.
    """
    id: str
    dosage: str
    advise: str
    dates: List[str]
    name: str = ""  # Add this line to include the name of the medication

@dataclass
class TimeSheetModel(BaseModel):
    """
    A data model representing a timesheet for medications.

    Attributes:
        id (str): The unique identifier of the timesheet.
        user_id (str): The ID of the user associated with the timesheet.
        medications (List[MedicationEntry]): A list of medications included in the timesheet.
        status (TimeSheetStatus): The status of the timesheet.
        start_date (str): The start date of the timesheet.
        end_date (str): The end date of the timesheet.
    """
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
        """
        Initialize a new TimeSheetModel instance.

        :param user_id: The ID of the user associated with the timesheet.
        :type user_id: str
        :param medications: A list of medications included in the timesheet.
        :type medications: List[MedicationEntry]
        :param status: The status of the timesheet.
        :type status: TimeSheetStatus
        :param start_date: The start date of the timesheet.
        :type start_date: str
        :param end_date: The end date of the timesheet.
        :type end_date: str
        :param _id: The unique identifier of the timesheet, default is -1.
        :type _id: int or str
        :param id: The unique identifier of the timesheet, default is -1 (redundant parameter).
        :type id: int or str
        """
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
        """
        Set the unique identifier for the timesheet.

        :param id: The unique identifier to set.
        :type id: int or str
        """
        self._id = id

    def get_id(self):
        """
        Get the unique identifier of the timesheet.

        :return: The unique identifier of the timesheet.
        :rtype: str
        """
        return str(self._id)

    def asdict(self):
        """
        Convert the TimeSheetModel instance to a dictionary.

        :return: A dictionary representation of the timesheet.
        :rtype: dict
        """
        dictionary = asdict(self)
        dictionary.update({'id': str(self._id)})
        dictionary['status'] = self.status
        dictionary['medications'] = [asdict(med) for med in self.medications]
        return dictionary

    def log(self):
        """
        Log the details of the timesheet using the logging module.
        """
        logging.info(f"TimeSheet: User ID: {self.user_id}, Status: {self.status.value}")
        for med in self.medications:
            logging.info(f"  Medication: {med.id}, Dosage: {med.dosage}, Dates: {med.dates}")
        logging.info(f"Advise: {self.advise}")
