from flask import Flask
from flask_cors import CORS
from auth.login_manager import init_login_manager
from routes.auth import auth as auth_routes
from routes.users import users as users_routes
from routes.medications import medications as medications_routes
from routes.timesheets import timesheets as timesheets_routes
from flask_injector import FlaskInjector
from injector import singleton
from services.medication_service import MedicationService
from controllers.medications_controller import MedicationsController

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Initialize the login manager for user authentication
init_login_manager(app)

# Register Blueprints for different parts of the application
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(users_routes, url_prefix='/users')
app.register_blueprint(medications_routes, url_prefix='/medications')
app.register_blueprint(timesheets_routes, url_prefix='/timesheets')

def configure(binder):
    """
    Configure dependency injection bindings.

    Args:
        binder: The dependency injection binder to bind services and controllers.
    """
    binder.bind(MedicationService, to=MedicationService, scope=singleton)
    binder.bind(MedicationsController, to=MedicationsController, scope=singleton)

@app.route('/')
def home():
    """
    Home page route.

    Returns:
        str: HTML content for the home page with a link to the login page.
    """
    return 'Home Page - <a href="/auth/login">Login</a>'

# Integrate Flask with the Injector for dependency injection
FlaskInjector(app=app, modules=[configure])

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask development server with debug mode enabled
