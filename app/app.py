from flask import Flask
from flask_cors import CORS
from auth.login_manager import init_login_manager
from routes.auth import auth as auth_routes
from routes.users import users as users_routes
from routes.medications import medications as medications_routes

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)
init_login_manager(app)

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(users_routes, url_prefix='/users')
app.register_blueprint(medications_routes, url_prefix='/medications')

@app.route('/')
def home():
    return 'Home Page - <a href="/auth/login">Login</a>'

if __name__ == '__main__':
    app.run(debug=True)