# file to configure flask, loaded into our flask application
# using the line: app.config.from_pyfile("config.py") in website.py
from os import environ
import os

# These variables be available to your application to use.
# Things that may be different on different computers, like a path to a file,
# should go in here. This is all available in GitHub, so be careful.

# SECRET_KEY = 'secretkey'
SECRET_KEY = 'secretkey'
# SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
SECURITY_PASSWORD_SALT = 'my_precious_two'
EVENT_CONFIRMATION_SALT = 'my_precious_three'
MAIL_DEFAULT_SENDER = 'jarcmb2118@gmail.com'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USER')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# For example, you can add the port you wish to run on as a variable.
# This can then be used when running the code.
MY_PORT = "5000"
SECURITY_PASSWORD_SALT = 'my_precious_two'

# !!! Important !!!
# Anything written in this file is effectively public knowledge.
# Anything that should remain a secret, like a password for a database or an
# API Key, should *not* be written here in plain text.
# # Instead, these should be set as environment variables on the computer you
# are using, and then imported here.

# For example, an enviornment variable called "DB_PASSWORD" will be read from
# the computer's environment into the python flask environment when the
# application starts. In this setup, you can have a local database for testing
# with the password "my_amazing_password".
#
# You can set that in your terminal using:
#   $ export DB_PASSWORD="my_amazing_password" (macOS/Linux)
#   c: set  DB_PASSWORD="my_amazing_password" (Windows)
#
# You can then set a different password for your production database in GitHub,
# by adding it as a repository secret, like with our google cloud credentials.
# Those passwords can then be added dynamically to app.yaml by the GitHub
# Action step called "Prepare Deployment" on line 36 of main.yaml.
DATABASE_PASSWORD = environ.get('DB_PASSWORD')
