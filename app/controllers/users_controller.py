from model.user_model import UserModel
from db.users import Users
from flask import jsonify, request, make_response, redirect, url_for, flash, session
from services.password_encoder import PasswordEncoder
from flask_login import login_user, logout_user
from model.roles import Role
from pydantic import ValidationError, EmailStr
from typing import Dict
from email_validator import validate_email, EmailNotValidError


class UsersController:

    def create_user(self):
        data: Dict = request.get_json()

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
        try:
            user = UserModel(**data)
            user.email = email
            added_user = Users.add(user)
            return make_response(jsonify({"inserted_id": str(added_user._id)}), 201)
        except ValidationError as e:
            return make_response(jsonify(e.errors()), 422)

    def get_users(self):
        users = Users.findAll()
        for user in users:
            user["_id"] = str(
                user["_id"]
            )  # Convert ObjectId to string for JSON serialization
        return jsonify(users)

    def get_user(self, user_id):
        user = Users.find(user_id)
        if user:
            user["_id"] = str(
                user["_id"]
            )  # Convert ObjectId to string for JSON serialization
            return jsonify(user)
        return make_response(jsonify({"error": "user not found"}), 404)

    def update_user_email(self, user_id, email):
        try:
            updated_user = Users.update_useremail(user_id, email)
            return make_response(jsonify({"error": "user not found"}), 404)
        except ValidationError as e:
            return make_response(jsonify(e.errors()), 422)

    def delete_user(self, user_id):
        result = Users.delete(user_id)
        if result.deleted_count:
            return jsonify({"deleted_count": result.deleted_count})
        return make_response(jsonify({"error": "user not found"}), 404)

    def login_user(self, username, password):
        user = Users.find_by_username(username)
        if user:
            password_matches = PasswordEncoder.check_password(password, user.password)
            if password_matches:
                user_logged_in = login_user(user)
                if user_logged_in:
                    return (
                        jsonify({"user_id": str(user.id), "username": user.username, "email": user.email}),
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
        logout_user()
        return jsonify({"message": "Logged out successfully."})
