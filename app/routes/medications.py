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