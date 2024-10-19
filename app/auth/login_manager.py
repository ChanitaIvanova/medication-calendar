from flask_login import LoginManager, current_user
from db.users import Users
from functools import wraps
from flask import redirect, url_for, flash
from model.roles import Role

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database by their user ID.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        Users: The user object if found, otherwise None.
    """
    return Users.find(user_id)

def init_login_manager(app):
    """
    Initialize the login manager with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
def role_required(role: Role):
    """
    A decorator to restrict access to a view based on user roles.

    Args:
        role (Role): The role required to access the decorated view.

    Returns:
        function: The decorated function that checks for user authentication and role.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_user_authorized(role):
                flash('You do not have the required permissions to access this resource. Please log in with an authorized account.')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_user_authorized(role: Role):
    """
    Check if the current user is authenticated and has the required role.

    Args:
        role (Role): The role required to access the resource.

    Returns:
        bool: True if the user is authenticated and has the required role, False otherwise.
    """
    if not current_user.is_authenticated:
        return False
    if not hasattr(current_user, 'has_role'):
        return False
    return current_user.has_role(role)
