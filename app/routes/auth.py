from flask import Blueprint, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
from controllers.users_controller import UsersController
from auth.login_manager import role_required
from model.roles import Role

# Create a Blueprint for authentication-related routes
auth = Blueprint("auth", __name__)

# Initialize the UsersController instance
user_controller = UsersController()


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login requests.

    .. http:post:: /api/auth/login

        :param username: The username for login.
        :param password: The password for login.
        :resheader Content-Type: application/json
        :status 200: Login successful
        :status 403: Method not allowed or authentication failed

        **Example request**:

        .. sourcecode:: http

            POST /api/auth/login
            Content-Type: application/json

            {
                "username": "user1",
                "password": "password123"
            }

    - If the request method is POST, attempts to log in the user with provided credentials.
    - If the request method is GET or any other method, returns an error response.

    Returns:
        Response: A JSON response indicating success or error.
    """
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        return user_controller.login_user(username, password)
    return make_response(jsonify({"error": "Method Not allowed"}), 403)


@auth.route("/logout")
@login_required
def logout():
    """
    Handle user logout requests.

    .. http:get:: /api/auth/logout

        :resheader Content-Type: application/json
        :status 200: Logout successful

    Requires the user to be logged in.

    Returns:
        Response: A response indicating successful logout.
    """
    return user_controller.logout()


@auth.route("/protected")
@login_required
@role_required(Role.ADMIN)
def protected():
    """
    Access a protected route that requires the user to have ADMIN role.

    .. http:get:: /api/auth/protected

        :resheader Content-Type: text/plain
        :status 200: Access successful
        :status 403: Forbidden - User does not have ADMIN role

    Requires the user to be logged in and have the ADMIN role.

    Returns:
        str: A message indicating the logged-in user's ID.
    """
    return f"Logged in as: {current_user.id}"


@auth.route("/user")
@login_required
def get_user_id():
    """
    Get the current user's ID, username, and email.

    .. http:get:: /api/auth/user

        :resheader Content-Type: application/json
        :status 200: User details returned
        :status 401: User not logged in

    Requires the user to be logged in.

    Returns:
        Response: A JSON response with user details if authenticated, otherwise an error message.
    """
    if current_user.is_authenticated:
        return jsonify({"user_id": str(current_user.id), "username": current_user.username, "email": current_user.email}), 200
    else:
        return jsonify({"error": "User not logged in"}), 401


@auth.route("/sign-up", methods=["POST"])
def sign_up():
    """
    Handle user sign-up requests.

    .. http:post:: /api/auth/sign-up

        :resheader Content-Type: application/json
        :status 200: User created successfully
        :status 405: Method not allowed

    - If the request method is POST, attempts to create a new user.
    - If the request method is not POST, returns an error response.

    Returns:
        Response: A JSON response indicating success or error.
    """
    if request.method == "POST":
        return user_controller.create_user()
    return make_response(jsonify({"error": "Method Not Allowed"}), 405)
