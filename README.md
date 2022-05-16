# Project SKYD

This is the source code for project SKYD! This was built by Shakeel Khan and Yeshwanth Dhanasekar for the 2022 UWB Hacks the Cloud Hackathon.

# General Documentation

## Project Goals

This is our second hackathon, our first we did together was a weeklong, so part of the reason we participated is that we wanted to see what a 48-hour long hackathon looks like and how much we could accomplish with it. We also wanted to use this opportunity to learn a bit more about fullstack development, and possibly build something worthy of putting on our portfolios.

For the project itself, we created a Web app called UniAssist, that is designed to help college students. Being college students ourselves, we understand that college students have a lot on their plate, such as finding an internship or job, organizing their life around their schoolwork, budgeting their money and managing their student debt, organizing assignments, setting deadlines, and keeping track of grades. We set out to create an all-in-one app that solves all of this.

## Desired User Experience

This app is designed to help college students with all the tools necessary for them to have an easier time managing their finances and their education. With features like calendar, Todo list, and the upcoming addition of note taking; students can stay up to date and on track on school assignments and events. With the future inclusion of budget tracker and debt calculator, students can also manage how much money they spend on a week or monthly basis to promote smarter money spending. More features will increase the productivity and allow students to have an easier experience at college. 

## Implementation Details

We used the following tools for this project:
 * **Backend**: Python, Flask Web Framework, Boto3 API for accessing AWS.
 * **Middle**: AWS: DynamoDB, S3, Elastic Beanstalk, CloudFront CDN
 * **Frontend**: HTML + CSS, JavaScript.

### Backend

For the backend, we chose Python because we're most comfortable with it for web development. We chose Flask mostly because it was the only web development framework we knew, but also because it's super lightweight and easy to work with compared to something like Django.

Our Flask application was written using two blueprints: one in `auth.py` and the other in `main.py`. The former defined all the endpoints that deal with user session management (signing up, logging in/out) and the latter defined all the endpoints for the application (the Todo list, profile page, calendar, etc.). `application.py` is where the application is put together and configured, and `util.py` contains various helper methods for working with AWS - things like retrieving an S3 bucket or DynamoDB table.

### Middle

For the middle, we chose AWS because Shakeel, who did most of the backend work, had the most experience with AWS. We both know from experience that deploying to the cloud can be difficult at times, so we wanted to stick with something we knew so we could focus more on building the app and less on troubleshooting.

 * We chose DynamoDB because it's a NoSQL database, which means the schema is very flexible. This made things easier for us, as we often had to make several changes to the schema on the fly as we were building the application. We have 3 tables:
    * A table for storing the users and all their information. This includes the date they joined the service, a hash of their password, a link to their profile picture (stored in our S3 bucket), their name and email address.
    * A table for the calendar events.
    * And a table for the Todo-list, storing all the items per user.

 * We chose Elastic Beanstalk because it's super simple and it automatically does a lot for you - setting up an EC2 instances (your VM), setting up security groups and load balancers for your EC2 instances, as well as several other essential services for a web app. Deploying to it is as simple as running a single command in the terminal. Because of all this, we really felt no need to try something new.

 * We chose S3 because it's cheap, reliable, and has decent performance (at least for our needs). The S3 bucket is where we store the profile pictures of all the users. To increase performance of the bucket, we decided to use an CloudFront CDN distribution, which essentially caches the data within the S3 bucket, making retrieval much quicker.

### Frontend

The frontend was plain HTML and CSS with some JavaScript. We used some community-made CSS files to speed up the process of making things look nice. We didn't use anything fancy like Angular or React, but we did make use of Flask's templating engine, Jinja2, effectively creating HTML templates that would be rendered upon request. For example, on the profile page, we used the templating engine to place the user's name, email address, and profile picture, into the HTML template for the profile page before it is then returned to the user.

All the user interaction was done using HTML forms (as we weren't able to get the WebSocket working - this is discussed in the next section) in the frontend, that would perform a POST request to the backend with all the form information. The little JavaScript used was mainly for small animations.

## Issues Encountered

One of the issues encountered was trying to get [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) working. We attempted to do this using the Flask-SocketIO extension and SocketIO on the client side (JavaScript). While we were able to get this working locally, we couldn't get it to work in our Elastic Beanstalk environment. The WebSocket would connect, but it would disconnect every 30 seconds, and we weren't able to send any data (the server never picked anything up, there weren't even any error messages we could find). We really wanted to get this going because one of the reasons you use a WebSocket is that you can update things in real-time, you don't need to automatically refresh the page. We felt this would be better for the UX. We ended up spending too much time on this and weren't able to get it working (part of the issue was the sparse documentation for stuff like when working with AWS). This is something we'll definitely be investigating afterwards.

## Bugs

Here are the ongoing and fixed bugs.

### Fixed

 * 

### Ongoing

 * For some reason the logout button disappears when viewing the Todo list.

## Future Work

Almost all of this is what we originally set out for but weren't able to accomplish in the time frame.

 * Implementing the following features:
    * Notes.
    * Budget Tracker.
    * Debt Calculator.
 * Account settings page:
    * Adding functionality to update password.
    * Force the profile picture to always be round.
    * Have an edit icon appear when the mouse is hovered over the profile picture (to make it more obvious).
    * Ability to link Canvas account to pull assignments from for the To-Do list and calendar.
 * To-Do:
    * Ability to add date and time to task.
    * Ability to edit task.
    * Ability to have multiple lists.
 * Calendar:
    * Ability to have more than on event per day on Calendar.
    * Ability to set times on schedule.
    * Ability to view full schedule by selecting a day.
    * Ability to color code events.
    * Ability to edit events.
 * Better quality control over the UI (keeping colors, fonts, and general layout consistent throughout the site).
 * Huge refactoring to code - optimizing DB queries to minimize bandwidth and costs, cleaning up the HTML, CSS, and JS.
 * Working out WebSockets so adding an event or item on a to-do list can be done in real time, without refreshing the page.
 * A proper 404 page.

# Developer Documentation

## Credential Configuration

If you aren't one of the developers, ignore this. This section will go over how to configure your credentials to access the DynamoDB tables used for the project.

### What You Need to Provide Me (Shakeel)

All I need from you is your AWS account ID (this is for your root account, not one of the accounts you created in IAM). This can be accessed by clicking the your username in the upper right hand corner of the AWS management console.

### What You Need to Do

To gain access to DynamoDB, you need to follow the directions here: https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/configure-cross-account-access-to-amazon-dynamodb.html

Specifically, follow the directions from the table titled "Configure Access to Account A from Account B" (you are account B, I am account A). A few things to note:
 * You can name the policy (the first row in the table) and role (the second row in the table) anything, it doesn't matter.
 * When creating the policy you'll see it asking you to paste a JSON document in one part of the setup, paste this one instead:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::336154851508:role/dynamodb-full-access-role-test"
        }
    ]
}
```

 * Lastly, when creating the role (the second row), step **2** tells you to set the type of trusted entity to "AWS Service". Instead, you should select "AWS Account", and select "This account (your 12-digit account ID)" below. Skip step 3, and follow the remaining steps.

### Verifying Your Access

The first thing you need to do is clone the project repository, and checkout the `resource-testing` branch. You need to run the server **locally**. This can be done by running `./run` in the terminal.

If the applications starts and spits some errors, send me the error and we'll work it out.

Otherwise, if it starts just fine, then the tables should have been successfully retrieved. To be sure, go ahead an create an account or login (both require use of the DynamoDB table). If there is some error, let me know and we'll work it out.