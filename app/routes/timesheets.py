from flask import Blueprint
from controllers.timesheets_controller import TimesheetsController
from flask_login import login_required
from injector import inject

timesheets = Blueprint('timesheets', __name__)

@timesheets.route('/timesheet', methods=['POST'])
@login_required
@inject
def create_timesheet(timesheets_controller: TimesheetsController):
    """
    .. http:post:: /api/timesheets/timesheet

        Create a new timesheet.

        Requires user to be logged in.

        :param timesheets_controller: The controller used to create the timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Timesheet created successfully
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `TimesheetsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return timesheets_controller.create_timesheet()

@timesheets.route('/timesheets', methods=['GET'])
@login_required
@inject
def get_all_timesheets(timesheets_controller: TimesheetsController):
    """
    .. http:get:: /api/timesheets/timesheets

        Get all timesheets.

        Requires user to be logged in.

        :param timesheets_controller: The controller used to retrieve timesheets.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Successfully retrieved all timesheets
        :statuscode 401: Unauthorized

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `TimesheetsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return timesheets_controller.get_all_timesheets()

@timesheets.route('/timesheet/<id>', methods=['GET'])
@login_required
@inject
def get_timesheet_by_id(timesheets_controller: TimesheetsController, id):
    """
    .. http:get:: /api/timesheets/timesheet/{id}

        Get a timesheet by ID.

        Requires user to be logged in.

        :param id: The ID of the timesheet to retrieve.
        :type id: str
        :param timesheets_controller: The controller used to get the timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Successfully retrieved timesheet
        :statuscode 400: Bad request
        :statuscode 401: Unauthorized

        **Dependency Injection**: The `inject` decorator is used to automatically provide an instance of `TimesheetsController`. This improves code maintainability by decoupling dependencies and makes unit testing easier by allowing mock injections.

    """
    return timesheets_controller.get_timesheet_by_id(id)
