from model.medication_model import MedicationModel
from db.medications import Medications
from flask import jsonify, request, make_response
from typing import Dict
from flask_login import current_user
from services.medication_service import MedicationService
from injector import inject
import json

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

    def get_medications_for_user(self, page, per_page, sort_field=None, sort_direction=None, **filters):
        user_id = str(current_user.id)
        total_count, medications = Medications.find_by_user_id(
            user_id, page, per_page, sort_field, sort_direction, filters
        )
        return jsonify({
            'medications': [json.loads(MedicationModel(**med).to_json()) for med in medications],
            'total_count': total_count,
            'page': page,
            'per_page': per_page
        })

    def get_medication(self, medication_id):
        medication = Medications.find(medication_id)
        if medication:
            return jsonify(json.loads(medication.to_json()))
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

    def update_medication(self, medication_id):
        data: Dict = request.get_json()
        user_id = str(current_user.id)
        
        medication = Medications.find(medication_id)
        if not medication or medication.user_id != user_id:
            return make_response(jsonify({"error": "Medication not found or unauthorized"}), 404)
        
        updated_medication = MedicationModel(
            name=data['name'],
            contents=data['contents'],
            objective=data['objective'],
            side_effects=data['sideEffects'],
            dosage_schedule=data['dosageSchedule'],
            user_id=user_id,
            _id=medication_id
        )
        
        result = Medications.update(updated_medication)
        if result.modified_count:
            return jsonify({"message": "Medication updated successfully"}), 200
        return make_response(jsonify({"error": "Failed to update medication"}), 500)