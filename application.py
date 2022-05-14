# This file is where the application is built and run.

##########
# IMPORTS.
##########
from flask import Flask

# Constants.
SECRET_KEY = 'secret-key-goes-here'

####################
# BUILD APPLICATION.
####################
application = Flask(__name__)

# This has something to do with session management - idk what but DO NOT REMOVE.
application.config['SECRET_KEY'] = SECRET_KEY

@application.route('/')
def index():
    return 'Hello World!'

# Run the app.
if __name__ == '__main__':
    # TODO: Disable debugging for production.
    application.debug = True
    application.run()