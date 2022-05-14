# This file handles everything related to authentication, account creation, and session management.

##########
# IMPORTS.
##########
import datetime
today = datetime.date.today()   # This is a method we're importing.

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import usersTable
from models import User

############
# CONSTANTS.
############
PASSWORD_HASH_METHOD = 'sha256'

########
# SETUP.
########

# Define the auth blueprint. This has all the event handlers for handling session management.
auth = Blueprint('auth', __name__)

#################
# LOGIN HANDLERS.
#################
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # Grab the email, password, and whether they want their credentials to be remembered from the
    # HTML form.
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Check whether the user actually exists (user.id shouldn't be None), and if so, whether the
    # password is correct.
    user = User(usersTable, email)
    if (user.id != None and check_password_hash(user.passwordHash, password)):
        # The user has the right credentials.
        login_user(user, remember=remember)     # Starts the session.
        return redirect(url_for('main.profile'))
    else:
        # Incorrect credentials.
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

##################
# SIGNUP HANDLERS.
##################

# Determines whether a user exists - returns True if so else False.
def isValidEmail(email):
    user = User(usersTable, email)
    return (user.id == None)

# Creates a new user in the database. THIS WILL OVERWRITE ANY EXISTING ENTRY WITH THE SAME EMAIL.
# You must ensure the email and username are not already in use before calling this method.
def createUser(email, name, password):
    # Create their account into the actual DB.
    item = {
        'email': email,
        'name': name,
        'passwordHash': generate_password_hash(password, method=PASSWORD_HASH_METHOD),
        'joinDate': today.strftime("%b %d %Y"),
    }
    usersTable.put_item(Item = item)
    return User(usersTable, email)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # Grab the email, username and password from the HTML form.
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Verify the sign-up information is correct.
    if (not isValidEmail(email)):
        # Flash an error message and redirect to the signup.
        flash('Email address already in use')
        return redirect(url_for('auth.signup'))
    
    # Create the new user, adding the information to the database.
    createUser(email, name, password)

    # Send them to login with their new credentials.
    return redirect(url_for('auth.login'))

#################
# LOGOUT HANDLER.
#################
@auth.route('/logout')
@login_required
def logout():
    # End the user session and redirect to the landing page.
    logout_user()
    return redirect(url_for('main.index'))