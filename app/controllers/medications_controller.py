from model.medication_model import MedicationModel
from db.medications import Medications
from flask import jsonify, request, make_response
from typing import Dict
from flask_login import current_user, login_required
from services.medication_service import MedicationService
from services.timesheet_service import TimesheetService
from db.timesheets import Timesheets
from model.timesheet_model import TimeSheetModel, MedicationEntry
from injector import inject
import json

class MedicationsController:
    """
    Controller class for managing medication-related operations.
    """
    
    @inject
    def __init__(self, medication_service: MedicationService, timesheet_service: TimesheetService):
        """
        Initialize the MedicationsController with service instances.

        :param medication_service: The service used to manage medication-related operations.
        :param timesheet_service: The service used to manage timesheet-related operations.
        """
        self.medication_service = medication_service
        self.timesheet_service = timesheet_service

    def create_medication(self):
        """
        Create a new medication from JSON data.

        :return: A response indicating the success or failure of the medication creation.
        :rtype: Response
        :statuscode 201: Medication created successfully
        :statuscode 400: Bad request (e.g., invalid JSON format or missing required fields)
        """
        try:
            data: Dict = request.get_json()
            if data is None:
                return make_response(jsonify({"error": "Invalid JSON format"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400)
        return self.__create_medication(data)
    
    @inject
    def create_medication(self, file):
        """
        Create a new medication from an uploaded file.

        :param file: The uploaded file containing medication data.
        :type file: FileStorage
        :return: A response indicating the success or failure of the medication creation.
        :rtype: Response
        :statuscode 201: Medication created successfully
        :statuscode 400: Bad request (e.g., invalid file format or missing required fields)
        """
        data: Dict = self.medication_service.parse_medication_data(file)
        return self.__create_medication(data)

    def get_medications_for_user(self, page, per_page, sort_field=None, sort_direction=None, **filters):
        """
        Get a list of medications for the current user with optional filters and pagination.

        :param page: The page number for pagination.
        :type page: int
        :param per_page: The number of items per page.
        :type per_page: int
        :param sort_field: The field to sort results by.
        :type sort_field: str, optional
        :param sort_direction: The direction of sorting (asc or desc).
        :type sort_direction: str, optional
        :param filters: Optional filters for medication attributes.
        :type filters: dict
        :return: A JSON response containing the list of medications and pagination details.
        :rtype: Response
        :statuscode 200: Successfully retrieved medications
        :statuscode 400: Bad request (e.g., invalid pagination parameters)
        """
        try:
            page = int(page)
            per_page = int(per_page)
            if page < 1 or per_page < 1:
                return make_response(jsonify({"error": "Invalid pagination parameters"}), 400)
        except ValueError:
            return make_response(jsonify({"error": "Pagination parameters must be integers"}), 400)
        
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
        """
        Get a medication by its ID.

        :param medication_id: The ID of the medication to retrieve.
        :type medication_id: str
        :return: A JSON response containing the medication details.
        :rtype: Response
        :statuscode 200: Successfully retrieved medication
        :statuscode 404: Medication not found
        """
        medication = Medications.find(medication_id)
        if medication:
            return jsonify(json.loads(medication.to_json()))
        return make_response(jsonify({"error": "Medication not found"}), 404)

    def delete_medication(self, medication_id):
        """
        Delete a medication by its ID.

        :param medication_id: The ID of the medication to delete.
        :type medication_id: str
        :return: A response indicating the success or failure of the deletion.
        :rtype: Response
        :statuscode 200: Medication deleted successfully
        :statuscode 404: Medication not found
        """
        result = Medications.delete(medication_id)
        if result.deleted_count:
            self.__update_user_timesheet()
            return jsonify({"deleted_count": result.deleted_count})
        return make_response(jsonify({"error": "Medication not found"}), 404)
    
    def __create_medication(self, data: Dict):
        """
        Helper function to create a medication from given data.

        :param data: The medication data.
        :type data: dict
        :return: A response indicating the success or failure of the medication creation.
        :rtype: Response
        :statuscode 201: Medication created successfully
        :statuscode 400: Bad request (e.g., missing required fields)
        """
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
        self.__update_user_timesheet()
        return saved_medication.to_json(), 201

    def update_medication(self, medication_id):
        """
        Update a medication by its ID.

        :param medication_id: The ID of the medication to update.
        :type medication_id: str
        :return: A response indicating the success or failure of the medication update.
        :rtype: Response
        :statuscode 200: Medication updated successfully
        :statuscode 400: Bad request (e.g., invalid JSON format)
        :statuscode 404: Medication not found or unauthorized
        :statuscode 500: Failed to update medication
        """
        try:
            data: Dict = request.get_json()
            if data is None:
                return make_response(jsonify({"error": "Invalid JSON format"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400)
        
        user_id = str(current_user.id)
        
        medication = Medications.find(medication_id)
        if not medication or not hasattr(medication, 'user_id') or medication.user_id != user_id:
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
            self.__update_user_timesheet()
            return jsonify({"message": "Medication updated successfully"}), 200
        return make_response(jsonify({"error": "Failed to update medication"}), 500)

    @login_required
    def get_medications(self):
        """
        Get all medications.

        :return: A JSON response containing the list of all medications.
        :rtype: Response
        :statuscode 200: Successfully retrieved medications
        """
        medications = Medications.findAll()
        return jsonify([med.asdict() for med in medications])

    @login_required
    def get_user_medications(self):
        """
        Get all medications for the current user.

        :return: A JSON response containing the list of medications for the user.
        :rtype: Response
        :statuscode 200: Successfully retrieved user medications
        """
        user_id = str(current_user.id)
        medications = Medications.find_by_user_id(user_id)
        medications_dict = [MedicationModel(**med) for med in medications]
        return jsonify([{"id": str(med._id), "name": med.name} for med in medications_dict])

    def __update_user_timesheet(self):
        """
        Helper method to update or create user's timesheet after medication changes.
        """
        user_id = str(current_user.id)
        timesheets = Timesheets.find_by_user_id(user_id)
        
        # Get all user's medications
        medications = Medications.find_by_user_id(user_id)
        if not medications:
            # If user has no medications, delete any existing timesheet
            if timesheets:
                for ts in timesheets:
                    Timesheets.delete(ts.id)
            return
        medications_dict = [MedicationModel(**med) for med in medications]
        medication_ids = [str(med.id) for med in medications_dict]
        
        if not timesheets:
            # Create new timesheet if none exists
            from datetime import datetime, timedelta
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=30)  # Default to 30 days
            
            timesheet_data = {
                'medication_ids': medication_ids,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
            
            new_timesheet = self._build_timesheet(timesheet_data)
            Timesheets.add(new_timesheet)
        else:
            # Update existing timesheet with current medications
            for timesheet in timesheets:
                timesheet_data = {
                    'medication_ids': medication_ids,
                    'start_date': timesheet.start_date,
                    'end_date': timesheet.end_date
                }
                updated_timesheet = self._build_timesheet(timesheet_data)
                Timesheets.update(updated_timesheet)

    def _build_timesheet(self, data, user_id=None):
        """
        Build a timesheet based on provided data.

        :param data: Dictionary containing medication_ids, start_date, and end_date
        :param user_id: Optional user ID for the timesheet
        :return: A new TimeSheetModel instance
        """
        medication_ids = data['medication_ids']
        start_date = data['start_date']
        end_date = data['end_date']

        # Retrieve medications from the database
        medications = [Medications.find(med_id) for med_id in medication_ids]

        # Prepare data for timesheet service
        medications_data = [
            {
                "id": str(med.id),
                "name": med.name,
                "dosage_schedule": med.dosage_schedule,
                "objective": med.objective
            } for med in medications if med
        ]

        # Generate timesheet using service
        timesheet_data = self.timesheet_service.build_timesheet(
            medications_data, 
            start_date,
            end_date
        )

        # Create medication entries
        medication_entries = []
        for med in timesheet_data["medications"]:
            if med:
                medication_entries.append(
                    MedicationEntry(
                        id=med["id"],
                        dosage=med["dosage"],
                        dates=med["dates"],
                        advise=med["advise"]
                    )
                )

        return TimeSheetModel(
            user_id=user_id or str(current_user.id),
            medications=medication_entries,
            start_date=start_date,
            end_date=end_date
        )
