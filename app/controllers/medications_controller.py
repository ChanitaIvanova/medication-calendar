from model.medication_model import MedicationModel
from db.medications import Medications
from flask import jsonify, request, make_response
from typing import Dict
from flask_login import current_user
from services.medication_service import MedicationService
from injector import inject

class MedicationsController:
    
    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    def create_medication(self):
        data: Dict = request.get_json()
        return self.__create_medication(data)
    
    @inject
    def create_medication(self, file):
        data: Dict = self.medication_service.parse_medication_data(file)
        return self.__create_medication(data)

    def get_medications_for_user(self, user_id):
        medications = Medications.find_by_user_id(user_id)
        return jsonify(medications)

    def get_medication(self, medication_id):
        medication = Medications.find(medication_id)
        if medication:
            return medication.to_json()
        return make_response(jsonify({"error": "Medication not found"}), 404)

    def delete_medication(self, medication_id):
        result = Medications.delete(medication_id)
        if result.deleted_count:
            return jsonify({"deleted_count": result.deleted_count})
        return make_response(jsonify({"error": "Medication not found"}), 404)
    
    def __create_medication(self, data: Dict):
        required_fields = ['name', 'contents', 'objective', 'sideEffects', 'dosageSchedule']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return make_response(jsonify({"error": f"Missing required field: {field}"}), 400)
        
        medication = MedicationModel(
            name=data['name'],
            contents=data['contents'],
            objective=data['objective'],
            side_effects=data['sideEffects'],
            dosage_schedule=data['dosageSchedule'],
            user_id=str(current_user.id)
        )
        
        saved_medication = Medications.add(medication)
        return saved_medication.to_json(), 201