from flask import Blueprint, request
from controllers.medications_controller import MedicationsController
from flask_login import login_required
from injector import inject

medications = Blueprint('medications', __name__)

@medications.route('/medication', methods=['POST'])
@login_required
@inject
def create_medication(medications_controller: MedicationsController):
    return medications_controller.create_medication()

@medications.route('/medication/upload', methods=['POST'])
@login_required
@inject
def upload_medication(medications_controller: MedicationsController):
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file:
        return medications_controller.create_medication(file)

@medications.route('', methods=['GET'])
@login_required
@inject
def get_medications(medications_controller: MedicationsController):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_field = request.args.get('sort_field')
    sort_direction = request.args.get('sort_direction')
    
    # Get all filter parameters
    filters = {
        'name': request.args.get('name'),
        'contents': request.args.get('contents'),
        'objective': request.args.get('objective'),
        'side_effects': request.args.get('side_effects'),
        'dosage_schedule': request.args.get('dosage_schedule')
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    return medications_controller.get_medications_for_user(page, per_page, sort_field, sort_direction, **filters)