from dataclasses import dataclass, asdict


@dataclass
class MedicationModel:
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
        id=-1,
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.contents = contents
        self.objective = objective
        self.side_effects = side_effects
        self.dosage_schedule = dosage_schedule

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return str(self._id)

    def asdict(self):
        dictionary = asdict(self)
        dictionary.pop("id", None)
        print(dictionary)
        return dictionary

    def print(self):
        print(
            f"Medication: {self.name}/nContents: {self.contents}/nObjective{self.objective}/nSide Effects: {self.side_effects}/nDosage: {self.dosage_schedule}"
        )
