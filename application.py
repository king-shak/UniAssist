# This file is where the application is built and run.

##########
# IMPORTS.
##########
from flask import Flask
from flask_login import LoginManager
from pathlib import Path

from auth import usersTable, auth as auth_blueprint
from main import main as main_blueprint
from models import User
from constants import SECRET_KEY, UPLOAD_FOLDER

####################
# BUILD APPLICATION.
####################
# First, make sure our upload folder exists.
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

application = Flask(__name__)   # Note this must be "application" for the EB env to pick it up.

# This has something to do with session management - idk what but DO NOT REMOVE.
application.config['SECRET_KEY'] = SECRET_KEY
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the login manager.
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

# This tells Flask how to find a specific user from the ID that is stored in their session
# cookie.
@login_manager.user_loader
def load_user(user_id):
    user = User(usersTable, user_id)
    if (user.id == None): return None
    else: return user

# Register blueprints.
application.register_blueprint(auth_blueprint)
application.register_blueprint(main_blueprint)

# Run the app.
if __name__ == '__main__':
    # TODO: Disable debugging for production.
    application.debug = True
    application.run()