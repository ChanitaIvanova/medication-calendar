from flask import Blueprint
from controllers.users_controller import UsersController
from flask_login import login_required
from auth.login_manager import role_required
from model.roles import Role

users = Blueprint('users', __name__)

user_controller = UsersController()

@users.route('/user', methods=['POST'])
def create_user():
    """
    .. http:post:: /api/users/user

        Create a new user.

        :statuscode 200: User created successfully
        :statuscode 400: Bad request

    """
    return user_controller.create_user()

@users.route('', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def get_users():
    """
    .. http:get:: /api/users

        Get all users.

        Requires user to be logged in and have ADMIN role.

        :statuscode 200: Successfully retrieved users
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden

    """
    return user_controller.get_users()

@users.route('/<string:user_id>', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def get_user(user_id):
    """
    .. http:get:: /api/users/{user_id}

        Get a user by ID.

        Requires user to be logged in and have ADMIN role.

        :param user_id: The ID of the user to retrieve.
        :type user_id: str
        :statuscode 200: Successfully retrieved user
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden

    """
    return user_controller.get_user(user_id)

@users.route('/<string:user_id>/email/<string:email>', methods=['PUT'])
def update_user_email(user_id, email):
    """
    .. http:put:: /api/users/{user_id}/email/{email}

        Update a user's email address.

        :param user_id: The ID of the user to update.
        :type user_id: str
        :param email: The new email address.
        :type email: str
        :statuscode 200: User email updated successfully
        :statuscode 400: Bad request

    """
    return user_controller.update_user_email(user_id, email)

@users.route('/<string:user_id>', methods=['DELETE'])
@login_required
@role_required(Role.ADMIN)
def delete_user(user_id):
    """
    .. http:delete:: /api/users/{user_id}

        Delete a user by ID.

        Requires user to be logged in and have ADMIN role.

        :param user_id: The ID of the user to delete.
        :type user_id: str
        :statuscode 200: User deleted successfully
        :statuscode 401: Unauthorized
        :statuscode 403: Forbidden

    """
    return user_controller.delete_user(user_id)