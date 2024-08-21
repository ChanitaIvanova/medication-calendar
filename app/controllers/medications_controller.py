from model.medication_model import MedicationModel
from db.medications import Medications
from flask import jsonify, request, make_response
from typing import Dict
from flask_login import current_user

class MedicationsController:

    def create_medicine(self):
        data: Dict = request.get_json()
        
        # Define required fields
        required_fields = ['name', 'contents', 'objective', 'sideEffects', 'dosageSchedule']
        
        # Validate required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return make_response(jsonify({"error": f"Missing required field: {field}"}), 400)
        
        # Create MedicationModel instance
        medication = MedicationModel(
            name=data['name'],
            contents=data['contents'],
            objective=data['objective'],
            side_effects=data['sideEffects'],
            dosage_schedule=data['dosageSchedule'],
            user_id=str(current_user.id)
        )
        
        # Save medication to database
        saved_medication = Medications.add(medication)
        
        # Return the saved medication data
        return jsonify({
            "id": saved_medication.get_id(),
            "name": saved_medication.name,
            "contents": saved_medication.contents,
            "objective": saved_medication.objective,
            "sideEffects": saved_medication.side_effects,
            "dosageSchedule": saved_medication.dosage_schedule,
            "userId": saved_medication.user_id
        }), 201

    def get_medications_for_user(self, user_id):
        medications = Medications.find_by_user_id(user_id)
        return jsonify(medications)

    def get_medication(self, medication_id):
        medication = Medications.find(medication_id)
        if medication:
            # Convert ObjectId to string for JSON serialization
            medication["_id"] = str(
                medication["_id"]
            )
            return jsonify(medication)
        return make_response(jsonify({"error": "Medication not found"}), 404)

    def delete_medication(self, medication_id):
        result = Medications.delete(medication_id)
        if result.deleted_count:
            return jsonify({"deleted_count": result.deleted_count})
        return make_response(jsonify({"error": "Medication not found"}), 404)