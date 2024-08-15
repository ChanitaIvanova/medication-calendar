from flask import Blueprint
from controllers.users_controller import UsersController
from flask_login import login_required
from auth.login_manager import role_required
from model.roles import Role

users = Blueprint('users', __name__)

user_controller = UsersController()

@users.route('/user', methods=['POST'])
def create_user():
    return user_controller.create_user()

@users.route('', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def get_users():
    return user_controller.get_users()

@users.route('/<string:user_id>', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def get_user(user_id):
    return user_controller.get_user(user_id)

@users.route('/<string:user_id>/email/<string:email>', methods=['PUT'])
def update_user_email(user_id, email):
    return user_controller.update_user_email(user_id, email)

@users.route('/<string:user_id>', methods=['DELETE'])
@login_required
@role_required(Role.ADMIN)
def delete_user(user_id):
    return user_controller.delete_user(user_id)