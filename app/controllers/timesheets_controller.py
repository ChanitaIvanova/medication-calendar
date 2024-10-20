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

class TimesheetsController:
    """
    Controller class for managing timesheet-related operations.
    """
    
    @inject
    def __init__(self, medication_service: MedicationService, timesheet_service: TimesheetService):
        """
        Initialize the TimesheetsController with MedicationService and TimesheetService instances.

        :param medication_service: The service used to manage medication-related operations.
        :type medication_service: MedicationService
        :param timesheet_service: The service used to manage timesheet-related operations.
        :type timesheet_service: TimesheetService
        """
        self.medication_service = medication_service
        self.timesheet_service = timesheet_service

    def create_timesheet(self):
        """
        Create a new timesheet for the current user based on provided medication IDs and date range.

        :return: A response indicating the success or failure of the timesheet creation.
        :rtype: Response
        :statuscode 201: Timesheet created successfully
        :statuscode 400: Bad request (e.g., missing required fields or invalid date format)
        """
        data: Dict = request.get_json()
        
        # Validate required fields
        required_fields = ['medication_ids', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return make_response(jsonify({"error": f"Missing required field: {field}"}), 400)
        
        # Build and save the new timesheet
        new_timesheet = self._build_timesheet(data)
        saved_timesheet = Timesheets.add(new_timesheet)
        return jsonify(saved_timesheet.asdict()), 201

    def get_all_timesheets(self):
        """
        Get all timesheets for the current user.

        :return: A JSON response containing the list of all timesheets for the user.
        :rtype: Response
        :statuscode 200: Successfully retrieved timesheets
        """
        user_id = str(current_user.id)  # Get the current user's ID
        timesheets = Timesheets.find_by_user_id(user_id)  # Fetch timesheets for the current user
        
        # Fetch medication names and link them to each medication entry
        for ts in timesheets:
            medication_ids = [med.id for med in ts.medications]
            medications = Medications.find_by_ids(medication_ids)
            medication_dict = {med.id: med.name for med in medications}
            
            for med_entry in ts.medications:
                med_entry.name = medication_dict.get(med_entry.id)  # Link name to each medication entry
        
        return jsonify([ts.asdict() for ts in timesheets]), 200

    def get_timesheet_by_id(self, id):
        """
        Get a timesheet by its ID.

        :param id: The ID of the timesheet to retrieve.
        :type id: str
        :return: A JSON response containing the timesheet details.
        :rtype: Response
        :statuscode 200: Successfully retrieved timesheet
        :statuscode 404: Timesheet not found
        """
        timesheet = Timesheets.find(id)
        if timesheet:
            medication_ids = [med.id for med in timesheet.medications]
            medications = Medications.find_by_ids(medication_ids)
            medication_dict = {str(med.id): med.name for med in medications}
            
            for med_entry in timesheet.medications:
                med_entry.name = medication_dict.get(med_entry.id)  # Link name to each medication entry
            
            return jsonify(timesheet.asdict()), 200
        return make_response(jsonify({"error": "Timesheet not found"}), 404)

    def delete_timesheet(self, id):
        """
        Delete a timesheet by its ID.

        :param id: The ID of the timesheet to delete.
        :type id: str
        :return: A response indicating the success or failure of the delete operation.
        :rtype: Response
        :statuscode 204: Timesheet deleted successfully
        :statuscode 404: Timesheet not found
        """
        try:
            Timesheets.delete(id)
            return make_response('', 204)
        except ValueError:
            return make_response(jsonify({"error": "Timesheet not found"}), 404)

    def edit_timesheet(self, id):
        """
        Edit an existing timesheet.

        :param id: The ID of the timesheet to edit.
        :type id: str
        :return: A response indicating the success or failure of the edit operation.
        :rtype: Response
        :statuscode 200: Timesheet updated successfully
        :statuscode 404: Timesheet not found
        """
        data = request.get_json()
        # Validate required fields
        required_fields = ['medication_ids', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return make_response(jsonify({"error": f"Missing required field: {field}"}), 400)

        # Fetch the existing timesheet
        existing_timesheet = Timesheets.find(id)
        if not existing_timesheet:
            return make_response(jsonify({"error": "Timesheet not found"}), 404)

        # Build a new timesheet with updated data
        new_timesheet = self._build_timesheet(data, existing_timesheet.user_id)
        
        # Save the new timesheet and delete the old one
        Timesheets.add(new_timesheet)
        Timesheets.delete(id)

        return jsonify(new_timesheet.asdict()), 200

    def _build_timesheet(self, data, user_id=None):
        """
        Build a timesheet based on provided data.

        :param data: The data containing medication IDs and date range.
        :param user_id: The user ID for the timesheet (optional for editing).
        :return: A new TimeSheetModel instance.
        """
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

        medication_entries = []
        # Parse OpenAI response and create MedicationEntry objects
        for med in data["medications"]:
            if med:
                medication_entries.append(MedicationEntry(id=med["id"], dosage=med["dosage"], dates=med["dates"], advise=med["advise"]))

        # Create and return the new timesheet
        return TimeSheetModel(
            user_id=user_id or str(current_user.id),
            medications=medication_entries,
            start_date=start_date_str,
            end_date=end_date_str,
            status=TimeSheetStatus.ACTIVE.value
        )

    def get_active_timesheet(self):
        """
        Get the first active timesheet for the current user.

        :return: A JSON response containing the active timesheet details or a message if none exists.
        :rtype: Response
        :statuscode 200: Successfully retrieved active timesheet
        :statuscode 404: No active timesheet found
        """
        user_id = str(current_user.id)  # Get the current user's ID
        timesheets = Timesheets.find_by_user_id(user_id)  # Fetch timesheets for the current user
        
        active_timesheet = next((ts for ts in timesheets if ts.status == TimeSheetStatus.ACTIVE.value), None)
        
        if active_timesheet:
            # Fetch medication names and link them to each medication entry
            medication_ids = [med.id for med in active_timesheet.medications]
            medications = Medications.find_by_ids(medication_ids)
            medication_dict = {str(med.id): med.name for med in medications}
            
            for med_entry in active_timesheet.medications:
                med_entry.name = medication_dict.get(med_entry.id)  # Link name to each medication entry
            
            return jsonify(active_timesheet.asdict()), 200
        
        return make_response(jsonify({"message": "No active timesheet found."}), 404)
