# This is where the meat of the application is defined - i.e., the endpoints for
# viewing/creating memes.

##########
# IMPORTS.
##########
from crypt import methods
import datetime
import hashlib
import json
import os
import random
import boto3
from boto3.dynamodb.conditions import Attr
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from util import getCDNURLForS3Object, retrieveBucket, retrieveTable, getKeyFromCDNURL
from constants import BUCKET_NAME, BUCKET_CDN_DOMAIN, PROFILE_PIC_ACL, USERS_TABLE_NAME, ALLOWED_EXTENSIONS, DEFAULT_PROFILE_PIC

################
# AWS RESOURCES.
################

# Retrieve the bucket.
s3 = boto3.resource('s3')
bucket = retrieveBucket(s3, BUCKET_NAME)

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
    return render_template('profile.html', name=current_user.name,
                                            email=current_user.id,
                                            profilePicURL=current_user.profilePicURL)

@main.route('/updateProfilePic', methods=['POST'])
@login_required
def updateProfilePic():
    file = request.files['file']
    if (file.filename == ''):   # No file was selected.
        return redirect(url_for('main.profile'))
    
    # We're good to go - upload the file.
    filename = secure_filename(file.filename)
    filepath = f'upload/{filename}'
    split = os.path.splitext(filepath)
    fileKey = f'profilepics/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + split[1]}'
    file.save(filepath)

    # Remove the existing file from the bucket, if it isn't the default.
    defaultProfilePicURL = getCDNURLForS3Object(BUCKET_CDN_DOMAIN, DEFAULT_PROFILE_PIC)
    if (current_user.profilePicURL != defaultProfilePicURL):
        deleteKey = getKeyFromCDNURL(current_user.profilePicURL)
        s3.Object(BUCKET_NAME, deleteKey).delete()
    
    # Upload the new file, remove it locally.
    bucket.upload_file(filepath, fileKey, ExtraArgs = {'ACL': 'public-read'})
    os.remove(filepath)

    # Update the user.
    newURL = getCDNURLForS3Object(BUCKET_CDN_DOMAIN, fileKey)
    current_user.updateProfilePicURL(usersTable, newURL)

    # Redirect to the profile page.
    return redirect(url_for('main.profile'))