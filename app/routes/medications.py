from flask import Blueprint, request
from controllers.medications_controller import MedicationsController
from flask_login import login_required
from injector import inject
from auth.login_manager import role_required
from model.roles import Role

medications = Blueprint('medications', __name__)

@medications.route('/medication', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
@inject
def create_medication(medications_controller: MedicationsController):
    """
    .. http:post:: /api/medications/medication

        Create a new medication.

        Requires user to be logged in and have ADMIN role.

        :param medications_controller: The controller used to create the medication.
        :type medications_controller: MedicationsController
        :statuscode 200: Medication created successfully
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden - User is not an admin

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return medications_controller.create_medication()

@medications.route('/medication/upload', methods=['POST'])
@login_required
@role_required(Role.ADMIN)
@inject
def upload_medication(medications_controller: MedicationsController):
    """
    .. http:post:: /api/medications/medication/upload

        Upload a medication file.

        Requires user to be logged in and have ADMIN role.

        :param medications_controller: The controller used to create the medication from the uploaded file.
        :type medications_controller: MedicationsController
        :statuscode 200: Medication created successfully from file
        :statuscode 400: Bad request (e.g., missing file or empty filename)
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden - User is not an admin

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file:
        return medications_controller.create_medication(file)

@medications.route('/medication/<medication_id>', methods=['DELETE'])
@login_required
@role_required(Role.ADMIN)
@inject
def delete_medication(medication_id: str, medications_controller: MedicationsController):
    """
    .. http:delete:: /api/medications/medication/{medication_id}

        Delete a medication by ID.

        Requires user to be logged in and have ADMIN role.

        :param medication_id: The ID of the medication to delete.
        :type medication_id: str
        :param medications_controller: The controller used to delete the medication.
        :type medications_controller: MedicationsController
        :statuscode 200: Medication deleted successfully
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden - User is not an admin

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return medications_controller.delete_medication(medication_id)

@medications.route('/medication/<medication_id>', methods=['GET'])
@login_required
@inject
def get_medication(medication_id: str, medications_controller: MedicationsController):
    """
    .. http:get:: /api/medications/medication/{medication_id}

        Get a medication by ID.

        Requires user to be logged in.

        :param medication_id: The ID of the medication to retrieve.
        :type medication_id: str
        :param medications_controller: The controller used to get the medication.
        :type medications_controller: MedicationsController
        :statuscode 200: Successfully retrieved medication
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return medications_controller.get_medication(medication_id)

@medications.route('/medication/<medication_id>', methods=['PUT'])
@login_required
@role_required(Role.ADMIN)
@inject
def update_medication(medication_id: str, medications_controller: MedicationsController):
    """
    .. http:put:: /api/medications/medication/{medication_id}

        Update a medication by ID.

        Requires user to be logged in and have ADMIN role.

        :param medication_id: The ID of the medication to update.
        :type medication_id: str
        :param medications_controller: The controller used to update the medication.
        :type medications_controller: MedicationsController
        :statuscode 200: Medication updated successfully
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden - User is not an admin

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return medications_controller.update_medication(medication_id)

@medications.route('/medications/user', methods=['GET'])
@login_required
@inject
def get_user_medications(medications_controller: MedicationsController):
    """
    .. http:get:: /api/medications/medications/user

        Get medications assigned to the current user.

        Requires user to be logged in.

        :param medications_controller: The controller used to get medications for the user.
        :type medications_controller: MedicationsController
        :return: A JSON response containing:
            - medications: List of medications with their details and user-specific data
                - id: The ID of the user medication record
                - medication_id: The ID of the medication from the catalog
                - name: The name of the medication
                - contents: The contents of the medication
                - objective: The objective of the medication
                - side_effects: The side effects of the medication
                - dosage_schedule: The user's prescribed dosage schedule
                - start_date: When the user should start taking the medication
                - end_date: When the user should stop taking the medication
                - notes: Additional notes for the user
            - total_count: Total number of medications assigned to the user
        :rtype: Response
        :statuscode 200: Successfully retrieved user medications
        :statuscode 401: Unauthorized

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`.
    """
    return medications_controller.get_user_medications()

@medications.route('', methods=['GET'])
@login_required
@inject
def get_all_medications(medications_controller: MedicationsController):
    """
    .. http:get:: /api/medications

        Get a list of all medications in the system with optional filters and pagination.

        Requires user to be logged in.

        :param medications_controller: The controller used to retrieve all medications.
        :type medications_controller: MedicationsController
        :query page: The page number for pagination (default is 1).
        :query per_page: The number of items per page (default is 10).
        :query sort_field: The field to sort the results by.
        :query sort_direction: The direction of sorting (e.g., 'asc' or 'desc').
        :query filters: Optional filters for medication attributes (e.g., 'name', 'contents', etc.).
        :statuscode 200: Successfully retrieved medications
        :statuscode 401: Unauthorized
        :statuscode 400: Bad request

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `MedicationsController`.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_field = request.args.get('sort_field')
    sort_direction = request.args.get('sort_direction')
    
    # Get all filter parameters
    filters = {
        'name': request.args.get('name'),
        'contents': request.args.get('contents'),
        'objective': request.args.get('objective'),
        'side_effects': request.args.get('side_effects')
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    return medications_controller.get_all_medications(page, per_page, sort_field, sort_direction, **filters)
