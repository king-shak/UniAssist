# A bunch of constants. Originally, these were all over the various source files, so the idea with
# this is to make things clear and avoid circular imports.

SECRET_KEY = 'secret-key-goes-here'

PASSWORD_HASH_METHOD = 'sha256'

DEFAULT_PROFILE_PIC = 'profilepics/default-profile-pic.png'

UPLOAD_FOLDER = 'upload/'

BUCKET_NAME = 'project-skyd-store'
BUCKET_CDN_DOMAIN = 'https://d1puw8wiol6e24.cloudfront.net'
PROFILE_PIC_ACL = 'public-read'

USERS_TABLE_NAME = 'project-skyd-users-table'
TASKS_TABLE_NAME = 'project-skyd-tasks-table'
EVENTS_TABLE_NAME = 'project-skyd-events-table'

ALLOWED_EXTENSIONS = {'.png', '.jpg'}

# These are all used for connecting to the DynamoDB resource.
REGION_NAME = "us-west-2"
ROLE_ARN = "arn:aws:iam::336154851508:role/dynamodb-full-access-role-test"  # Hopefully we can use
                                                                            # the same one for all
                                                                            # of them...
ROLE_SESSION_NAME = "RoleSessionName"   # This can be anything.