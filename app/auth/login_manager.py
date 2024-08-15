from flask_login import LoginManager, current_user
from db.users import Users
from functools import wraps
from flask import redirect, url_for, flash
from model.roles import Role

login_manager = LoginManager()

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return Users.find(user_id)

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
def role_required(role: Role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(current_user)
            if not current_user.is_authenticated or not current_user.has_role(role):
                flash('You do not have access to this resource.')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator