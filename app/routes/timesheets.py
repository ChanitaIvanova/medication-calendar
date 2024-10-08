from flask import Blueprint
from controllers.timesheets_controller import TimesheetsController
from flask_login import login_required
from injector import inject

timesheets = Blueprint('timesheets', __name__)

@timesheets.route('/timesheet', methods=['POST'])
@login_required
@inject
def create_timesheet(timesheets_controller: TimesheetsController):
    return timesheets_controller.create_timesheet()

# ... (You can add more routes here for other timesheet operations)