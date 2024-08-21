from flask import Blueprint, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
from controllers.users_controller import UsersController
from auth.login_manager import role_required
from model.roles import Role

auth = Blueprint("auth", __name__)

user_controller = UsersController()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        return user_controller.login_user(username, password)
    return  make_response(jsonify({"error": "Method Not allowed"}), 403)


@auth.route("/logout")
@login_required
def logout():
    return user_controller.logout()


@auth.route("/protected")
@login_required
@role_required(Role.ADMIN)
def protected():
    return f"Logged in as: {current_user.id}"

@auth.route("/user")
@login_required
def get_user_id():
    if current_user.is_authenticated:
        return jsonify({"user_id": str(current_user.id), "username": current_user.username, "email": current_user.email }), 200
    else:
        return jsonify({"error": "User not logged in"}), 401

@auth.route("/sign-up", methods=["POST"])
def sign_up():
    if request.method == "POST":
        return user_controller.create_user()
    return make_response(jsonify({"error": "Method Not Allowed"}), 405)