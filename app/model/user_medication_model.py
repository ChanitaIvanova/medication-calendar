from dataclasses import dataclass, asdict
from .base_model import BaseModel
from datetime import datetime
import logging

@dataclass
class UserMedicationModel(BaseModel):
    """
    A data model representing a user's prescribed medication.

    Attributes:
        id (str): The unique identifier of the user medication record.
        user_id (str): The ID of the user taking the medication.
        medication_id (str): The ID of the medication from the catalog.
        dosage_schedule (str): The doctor's prescribed dosage schedule.
        start_date (datetime): The date when the medication should start.
        end_date (datetime): The date when the medication should end.
        notes (str): Additional notes for taking the medication.
    """
    id: str
    user_id: str
    medication_id: str
    dosage_schedule: str
    start_date: datetime
    end_date: datetime
    notes: str

    def __init__(
        self,
        user_id: str,
        medication_id: str,
        dosage_schedule: str,
        start_date: datetime,
        end_date: datetime,
        notes: str = "",
        _id=-1,
        id=-1
    ):
        """
        Initialize a new UserMedicationModel instance.

        :param user_id: The ID of the user taking the medication.
        :type user_id: str
        :param medication_id: The ID of the medication from the catalog.
        :type medication_id: str
        :param dosage_schedule: The doctor's prescribed dosage schedule.
        :type dosage_schedule: str
        :param start_date: The date when the medication should start.
        :type start_date: datetime
        :param end_date: The date when the medication should end.
        :type end_date: datetime
        :param notes: Additional notes for taking the medication (optional).
        :type notes: str
        :param _id: The unique identifier of the record, default is -1.
        :type _id: int or str
        :param id: The unique identifier of the record, default is -1 (redundant parameter).
        :type id: int or str
        """
        self._id = _id
        self.id = _id
        self.user_id = user_id
        self.medication_id = medication_id
        self.dosage_schedule = dosage_schedule
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes

    def set_id(self, id):
        """
        Set the unique identifier for the user medication record.

        :param id: The unique identifier to set.
        :type id: int or str
        """
        self._id = id

    def get_id(self):
        """
        Get the unique identifier of the user medication record.

        :return: The unique identifier of the record.
        :rtype: str
        """
        return str(self._id)

    def asdict(self):
        """
        Convert the UserMedicationModel instance to a dictionary.

        :return: A dictionary representation of the user medication record.
        :rtype: dict
        """
        dictionary = asdict(self)
        dictionary.update({
            'id': str(self._id),
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        })
        return dictionary

    def log(self):
        """
        Log the details of the user medication record using the logging module.
        """
        logging.info(
            f"User Medication Record:\nUser ID: {self.user_id}\n"
            f"Medication ID: {self.medication_id}\n"
            f"Dosage Schedule: {self.dosage_schedule}\n"
            f"Period: {self.start_date} to {self.end_date}\n"
            f"Notes: {self.notes}"
        ) 