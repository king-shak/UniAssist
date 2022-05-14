# Project SKYD

This is the source code for project SKYD! This was built by Shakeel Khan and Yeshwanth Dhanasekar for the 2022 UWB Hacks the Cloud Hackathon.

# General Documentation

## Project Goals

TODO: Fill this out.

## Desired User Experience

TODO: Fill this out.

## Implementation Details

TODO: Fill this out (this will take time).

## Issues Encountered

TODO: Fill this out. This should be done as we're going along.

## Bugs

Here are the ongoing and fixed bugs.

### Fixed

TODO: Fill this out. This should be done as we're going along.

### Ongoing

TODO: Fill this out. This should be done as we're going along.

## Future Work

TODO: Fill this out.

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