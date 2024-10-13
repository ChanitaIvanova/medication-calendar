from flask import jsonify, request, make_response
from typing import List, Dict
from flask_login import current_user
from services.medication_service import MedicationService
from services.timesheet_service import TimesheetService
from db.timesheets import Timesheets
from db.medications import Medications
from model.timesheet_model import TimeSheetModel, MedicationEntry, TimeSheetStatus
from injector import inject
from datetime import datetime
import json

class TimesheetsController:
    
    @inject
    def __init__(self, medication_service: MedicationService, timesheet_service: TimesheetService):
        self.medication_service = medication_service
        self.timesheet_service = timesheet_service

    def create_timesheet(self):
        data: Dict = request.get_json()
        
        # Validate required fields
        required_fields = ['medication_ids', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return make_response(jsonify({"error": f"Missing required field: {field}"}), 400)
        
        medication_ids: List[str] = data['medication_ids']
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # Retrieve medications from the database
        medications = [Medications.find(med_id) for med_id in medication_ids]
        
        # Prepare data for OpenAI
        medications_data = [
            {
                "id": str(med.id),
                "name": med.name,
                "dosage_schedule": med.dosage_schedule,
                "objective": med.objective
            } for med in medications if med
        ]
        
        start_date_str = start_date.isoformat() if hasattr(start_date, 'isoformat') else str(start_date)
        end_date_str = end_date.isoformat() if hasattr(end_date, 'isoformat') else str(end_date)
        
        # Generate timesheet using OpenAI
        data: Dict = self.timesheet_service.build_timesheet(medications_data, start_date_str, end_date_str)
        # print(json.dumps(data, indent=4))
        medications_timesheet = data["medications"]
        
        medication_entries = []
        # Parse OpenAI response and create MedicationEntry objects
        # This is a simplified version; you may need to adjust based on the actual OpenAI response format
        for med in medications_timesheet:
            if med:
                #dates.append(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S'))
                medication_entries.append(MedicationEntry(id=med["id"], dosage=med["dosage"], dates= med["dates"], advise = med["advise"]))
        
        # Create and save the new timesheet
        new_timesheet = TimeSheetModel(
            user_id=str(current_user.id),
            medications=medication_entries,
            start_date=start_date_str,
            end_date=end_date_str,
            status=TimeSheetStatus.ACTIVE
        )
        
        saved_timesheet = Timesheets.add(new_timesheet)
        return jsonify(saved_timesheet.asdict()), 201

    def get_all_timesheets(self):
        user_id = str(current_user.id)  # Get the current user's ID
        timesheets = Timesheets.find_by_user_id(user_id)  # Fetch timesheets for the current user
        return jsonify([ts.asdict() for ts in timesheets]), 200

    def get_timesheet_by_id(self, id):
        timesheet = Timesheets.find(id)
        return jsonify(timesheet.asdict()) if timesheet else make_response(jsonify({"error": "Timesheet not found"}), 404)
