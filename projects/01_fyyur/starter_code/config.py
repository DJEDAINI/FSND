import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# To Debug SQLALCHEMY Queries
# SQLALCHEMY_ECHO = True

# Connect to the database


# DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:toor@127.0.0.1:5432/fyyur'
