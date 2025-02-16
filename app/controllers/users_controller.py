from model.user_model import UserModel
from db.users import Users
from flask import jsonify, request, make_response, redirect, url_for, flash, session
from services.password_encoder import PasswordEncoder
from flask_login import login_user, logout_user
from pydantic import ValidationError, EmailStr
from typing import Dict
from email_validator import validate_email, EmailNotValidError
from model.roles import Role


class UsersController:
    """
    Controller class for managing user-related operations.
    """

    def create_user(self):
        """
        Create a new user.

        :return: A response indicating the success or failure of the user creation.
        :rtype: Response
        :statuscode 201: User created successfully
        :statuscode 400: Bad request (e.g., missing required fields or invalid JSON format)
        :statuscode 422: Unprocessable Entity (e.g., validation error)
        """
        try:
            data: Dict = request.get_json()
            if data is None:
                return make_response(jsonify({"error": "Invalid JSON format"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400)

        # Check if required fields are present
        required_fields = ["email", "username", "password"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return make_response(
                jsonify(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                400,
            )

        try:
            emailinfo = validate_email(data["email"], check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            return make_response(jsonify({"error": e}), 400)

        existing_user = Users.find_existing_user(email, data["username"])
        if existing_user:
            if existing_user["email"] == email:
                return make_response(jsonify({"error": "Email already exists"}), 400)
            else:
                return make_response(jsonify({"error": "Username already exists"}), 400)
        
        # Ensure role is set to USER by default
        data['role'] = Role.USER
        
        try:
            user = UserModel(**data)
            user.email = email
            added_user = Users.add(user)
            return make_response(jsonify({"inserted_id": str(added_user._id)}), 201)
        except ValidationError as e:
            return make_response(jsonify(e.errors()), 422)

    def get_users(self):
        """
        Get all users.

        :return: A JSON response containing the list of all users.
        :rtype: Response
        :statuscode 200: Successfully retrieved users
        """
        users = Users.findAll()
        users_dict = [user.to_json() for user in users]
        return jsonify(users_dict)

    def get_user(self, user_id):
        """
        Get a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :type user_id: str
        :return: A JSON response containing the user details.
        :rtype: Response
        :statuscode 200: Successfully retrieved user
        :statuscode 404: User not found
        """
        user = Users.find(user_id)
        if user:
            return user.to_json()
        return make_response(jsonify({"error": "user not found"}), 404)

    def update_user_email(self, user_id, email):
        """
        Update a user's email address.

        :param user_id: The ID of the user to update.
        :type user_id: str
        :param email: The new email address.
        :type email: str
        :return: A response indicating the success or failure of the email update.
        :rtype: Response
        :statuscode 404: User not found
        :statuscode 422: Unprocessable Entity (e.g., validation error)
        """
        try:
            updated_user = Users.update_useremail(user_id, email)
            return make_response(jsonify({"error": "user not found"}), 404)
        except ValidationError as e:
            return make_response(jsonify(e.errors()), 422)

    def delete_user(self, user_id):
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete.
        :type user_id: str
        :return: A response indicating the success or failure of the deletion.
        :rtype: Response
        :statuscode 200: User deleted successfully
        :statuscode 404: User not found
        """
        result = Users.delete(user_id)
        if result.deleted_count:
            return jsonify({"deleted_count": result.deleted_count})
        return make_response(jsonify({"error": "user not found"}), 404)

    def login_user(self, username, password):
        """
        Log in a user with their username and password.

        :param username: The username of the user.
        :type username: str
        :param password: The password of the user.
        :type password: str
        :return: A JSON response containing the user details if login is successful.
        :rtype: Response
        :statuscode 200: Successfully logged in
        :statuscode 401: Invalid username or password
        :statuscode 404: User not found
        """
        user = Users.find_by_username(username)
        if user:
            password_matches = PasswordEncoder.check_password(password, user.password)
            if password_matches:
                user_logged_in = login_user(user)
                if user_logged_in:
                    return (
                        jsonify({
                            "user_id": str(user.id), 
                            "username": user.username, 
                            "email": user.email,
                            "role": user.role.value
                        }),
                        200,
                    )
                else:
                    return make_response(
                        jsonify({"error": "Invalid username or password."}), 401
                    )
            else:
                return make_response(
                    jsonify({"error": "Invalid username or password."}), 401
                )
        return make_response(jsonify({"error": "User not found"}), 404)

    def logout(self):
        """
        Log out the current user.

        :return: A response indicating that the user has been logged out successfully.
        :rtype: Response
        :statuscode 200: Successfully logged out
        """
        logout_user()
        return jsonify({"message": "Logged out successfully."})
