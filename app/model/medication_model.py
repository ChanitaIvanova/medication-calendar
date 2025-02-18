from dataclasses import dataclass, asdict
from .base_model import BaseModel
import logging

@dataclass
class MedicationModel(BaseModel):
    """
    A data model representing a medication in the system catalog.

    Attributes:
        id (str): The unique identifier of the medication.
        user_id (str): The ID of the admin user who added the medication.
        name (str): The name of the medication.
        contents (str): The contents or ingredients of the medication.
        objective (str): The objective or purpose of the medication.
        side_effects (str): The potential side effects of the medication.
        dosage_schedule (str): The dosage schedule for the medication.
    """
    id: str
    user_id: str
    name: str
    contents: str
    objective: str
    side_effects: str
    dosage_schedule: str
    def __init__(
        self,
        name: str,
        contents: str,
        objective: str,
        side_effects: str,
        dosage_schedule: str,
        user_id: str,
        _id=-1,
        id=-1
    ):
        """
        Initialize a new MedicationModel instance.

        :param name: The name of the medication.
        :type name: str
        :param contents: The contents or ingredients of the medication.
        :type contents: str
        :param objective: The objective or purpose of the medication.
        :type objective: str
        :param side_effects: The potential side effects of the medication.
        :type side_effects: str
        :param dosage_schedule: The dosage schedule for the medication.
        :type dosage_schedule: str
        :param user_id: The ID of the admin user who added the medication.
        :type user_id: str
        :param _id: The unique identifier of the medication, default is -1.
        :type _id: int or str
        :param id: The unique identifier of the medication, default is -1 (redundant parameter).
        :type id: int or str
        """
        self._id = _id
        self.id = _id
        self.user_id = user_id
        self.name = name
        self.contents = contents
        self.objective = objective
        self.side_effects = side_effects
        self.dosage_schedule = dosage_schedule

    def set_id(self, id):
        """
        Set the unique identifier for the medication.

        :param id: The unique identifier to set.
        :type id: int or str
        """
        self._id = id

    def get_id(self):
        """
        Get the unique identifier of the medication.

        :return: The unique identifier of the medication.
        :rtype: str
        """
        return str(self._id)

    def asdict(self):
        """
        Convert the MedicationModel instance to a dictionary.

        :return: A dictionary representation of the medication.
        :rtype: dict
        """
        dictionary = asdict(self)
        dictionary.update({'id': str(self._id)})
        return dictionary

    def log(self):
        """
        Log the details of the medication using the logging module.
        """
        logging.info(
            f"Medication: {self.name}\nAdded by: {self.user_id}\n"
            f"Contents: {self.contents}\nObjective: {self.objective}\n"
            f"Side Effects: {self.side_effects}\nDosage Schedule: {self.dosage_schedule}"
        )
