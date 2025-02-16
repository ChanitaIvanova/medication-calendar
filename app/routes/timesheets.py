from flask import Blueprint
from controllers.timesheets_controller import TimesheetsController
from flask_login import login_required
from injector import inject

timesheets = Blueprint('timesheets', __name__)

@timesheets.route('/timesheet', methods=['GET'])
@login_required
@inject
def get_timesheet(timesheets_controller: TimesheetsController):
    """
    .. http:get:: /api/timesheets/timesheet

        Get the user's timesheet.

        Requires user to be logged in.

        :param timesheets_controller: The controller used to retrieve the timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Successfully retrieved timesheet
        :statuscode 404: No timesheet found
    """
    return timesheets_controller.get_timesheet()

@timesheets.route('/timesheet', methods=['PUT'])
@login_required
@inject
def update_timesheet(timesheets_controller: TimesheetsController):
    """
    .. http:put:: /api/timesheets/timesheet

        Create or update the user's timesheet.

        Requires user to be logged in.

        :param timesheets_controller: The controller used to update the timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Timesheet updated successfully
        :statuscode 400: Bad request
    """
    return timesheets_controller.update_timesheet()

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

@timesheets.route('/timesheet/<id>', methods=['DELETE'])
@login_required
@inject
def delete_timesheet(timesheets_controller: TimesheetsController, id):
    """
    .. http:delete:: /api/timesheets/timesheet/{id}

        Delete a timesheet by ID.

        Requires user to be logged in.

        :param id: The ID of the timesheet to delete.
        :type id: str
        :statuscode 204: Timesheet deleted successfully
        :statuscode 404: Timesheet not found
    """
    return timesheets_controller.delete_timesheet(id)

@timesheets.route('/timesheet/<id>', methods=['PUT'])
@login_required
@inject
def edit_timesheet(timesheets_controller: TimesheetsController, id):
    """
    .. http:put:: /api/timesheets/timesheet/{id}

        Edit an existing timesheet.

        Requires user to be logged in.

        :param id: The ID of the timesheet to edit.
        :type id: str
        :param timesheets_controller: The controller used to edit the timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Timesheet updated successfully
        :statuscode 404: Timesheet not found
    """
    return timesheets_controller.edit_timesheet(id)

@timesheets.route('timesheet//active', methods=['GET'])  # New route for active timesheet
@login_required
@inject
def get_active_timesheet(timesheets_controller: TimesheetsController):
    """
    .. http:get:: /api/timesheets/timesheet/active

        Get the first active timesheet for the current user.

        Requires user to be logged in.

        :param timesheets_controller: The controller used to retrieve the active timesheet.
        :type timesheets_controller: TimesheetsController
        :statuscode 200: Successfully retrieved active timesheet
        :statuscode 404: No active timesheet found
    """
    return timesheets_controller.get_timesheet()
