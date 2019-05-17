import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'start123'
MYSQL_CURSORCLASS = 'DictCursor'
SECRET_KEY = 'secret123'

# SQLAlchemy stuff
SQLALCHEMY_DATABASE_URI = 'mysql://root:start123@localhost/challp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:start123@localhost:5433/challp'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Secure and unique secret key for signing the data
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'
