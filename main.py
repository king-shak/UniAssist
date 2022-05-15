# This is where the meat of the application is defined - i.e., the endpoints for
# viewing/creating memes.

##########
# IMPORTS.
##########
from asyncio import events
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
from constants import BUCKET_NAME, BUCKET_CDN_DOMAIN, PROFILE_PIC_ACL, USERS_TABLE_NAME, EVENTS_TABLE_NAME, TASKS_TABLE_NAME, ALLOWED_EXTENSIONS, DEFAULT_PROFILE_PIC

################
# AWS RESOURCES.
################

# Retrieve the bucket.
s3 = boto3.resource('s3')
bucket = retrieveBucket(s3, BUCKET_NAME)

# Grab the tables.
usersTable = retrieveTable(USERS_TABLE_NAME)
tasksTable = retrieveTable(TASKS_TABLE_NAME)
eventsTable = retrieveTable(EVENTS_TABLE_NAME)

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

@main.route('/nav')
def nav():
    return render_template('nav.html', tasks=None)

#################
# BUDGET HANDLER.
#################

@main.route('/budget')
def budget():
    return render_template('budget.html')

###################
# CALENDAR HANDLER.
###################

def retrieveEvents(eventsTable, userID):
    response = eventsTable.get_item(Key = {'email': userID})
    events = None
    if ('Item' in response): events = response['Item']['events']
    if (events != None and len(events) == 0): events = None
    return events

@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', events=retrieveEvents(eventsTable, current_user.id))

@main.route('/addEvent', methods=['POST'])
@login_required
def addEvent():
    # Retrieve the data from the form.
    title = request.form['title']
    date = request.form['date']
    newEvent = {'date': date, 'title': title}

    # Add this event to the existing list of events.
    events = retrieveEvents(eventsTable, current_user.id)
    if (events == None): events = [newEvent]
    else: events.append(newEvent)

    # Update the table.
    item = {
        'email': current_user.id,
        'events': events
    }
    eventsTable.put_item(Item = item)
    
    # Redirect back to the calendar page.
    return redirect(url_for('main.calendar'))

@main.route('/removeEvent', methods=['POST'])
@login_required
def removeEvent():
    # Retrieve the data from the form.
    date = request.form['dDate']

    # Remove this event from the current list of events.
    events = retrieveEvents(eventsTable, current_user.id)
    events = [e for e in events if e['date'] != date]

    # Update the table.
    item = {
        'email': current_user.id,
        'events': events
    }
    eventsTable.put_item(Item = item)
    
    # Redirect back to the calendar page.
    return redirect(url_for('main.calendar'))

################
# TO-DO HANDLER.
################

def retrieveTasks(tasksTable, userID):
    response = tasksTable.get_item(Key = {'email': userID})
    tasks = None
    if ('Item' in response): tasks = response['Item']['tasks']
    if (tasks != None and len(tasks) == 0): tasks = None
    return tasks

@main.route('/viewTasks')
@login_required
def viewTasks():
    # Render and return the template.
    return render_template('todo.html', tasks=retrieveTasks(tasksTable, current_user.id))

@main.route('/addTask', methods=['POST'])
@login_required
def addTask():
    # Grab/form all the information.
    taskName = request.form['new-task-input']
    timestamp = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")}'.encode('utf-8')
    taskURI = str(hashlib.md5(timestamp).hexdigest())
    newTask = [taskURI, taskName]

    # Add this task to the existing list of tasks.
    tasks = retrieveTasks(tasksTable, current_user.id)
    if (tasks == None): tasks = [newTask]
    else: tasks.append(newTask)

    # Update the table.
    item = {
        'email': current_user.id,
        'tasks': tasks
    }
    tasksTable.put_item(Item = item)

    # Redirect them to the viewTasks endpoint.
    return redirect(url_for('main.viewTasks'))

@main.route('/deleteTask/<taskURI>', methods=['POST'])
@login_required
def deleteTask(taskURI):
    # Retrieve the list of tasks, remove the one with the matching URI.
    tasks = retrieveTasks(tasksTable, current_user.id)
    if (tasks != None): tasks = [t for t in tasks if t[0] != taskURI]

    # Update the table.
    item = {
        'email': current_user.id,
        'tasks': tasks
    }
    tasksTable.put_item(Item = item)

    # Redirect them to the viewTasks endpoint.
    return redirect(url_for('main.viewTasks'))

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