# This is where the meat of the application is defined - i.e., the endpoints for
# viewing/creating memes.

##########
# IMPORTS.
##########
import datetime
import hashlib
import os
import random
import boto3
from boto3.dynamodb.conditions import Attr
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from util import retrieveTable

############
# CONSTANTS.
############
USERS_TABLE_NAME = "project-skyd-users-table"

################
# AWS RESOURCES.
################

# Grab the tables.
usersTable = retrieveTable(USERS_TABLE_NAME)
# TODO: Remaining tables.

#################
# MAIN DEFINITON.
#################
main = Blueprint('main', __name__)

###############################
# INDEX (LANDING PAGE) HANDLER.
###############################

@main.route('/')
def index():
    return render_template('index.html')

##################
# PROFILE HANDLER.
##################
@main.route('/profile')
@login_required
def profile():
    # Grab the user's meme and return them to the client.
    return render_template('profile.html', name=current_user.name)