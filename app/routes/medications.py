from flask import Blueprint
from controllers.medications_controller import MedicationsController
from flask_login import login_required

medications = Blueprint('medications', __name__)

medications_controller = MedicationsController()

@medications.route('/medication', methods=['POST'])
@login_required
def create_medication():
    return medications_controller.create_medicine()