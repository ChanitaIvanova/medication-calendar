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
app.secret_key = 'supersecretkey'
CORS(app)
init_login_manager(app)

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(users_routes, url_prefix='/users')
app.register_blueprint(medications_routes, url_prefix='/medications')
app.register_blueprint(timesheets_routes, url_prefix='/timesheets')

def configure(binder):
    binder.bind(MedicationService, to=MedicationService, scope=singleton)
    binder.bind(MedicationsController, to=MedicationsController, scope=singleton)

@app.route('/')
def home():
    return 'Home Page - <a href="/auth/login">Login</a>'

FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    app.run(debug=True)