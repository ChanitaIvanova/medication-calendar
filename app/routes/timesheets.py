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

@timesheets.route('/timesheets', methods=['GET'])
@login_required
@inject
def get_all_timesheets(timesheets_controller: TimesheetsController):
    return timesheets_controller.get_all_timesheets()

@timesheets.route('/timesheet/<id>', methods=['GET'])
@login_required
@inject
def get_timesheet_by_id(timesheets_controller: TimesheetsController, id):
    return timesheets_controller.get_timesheet_by_id(id)

# ... (You can add more routes here for other timesheet operations)
