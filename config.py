__author__ = 'cybran'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example


from mongoengine import connect

connect("MONGODB_DB", host='mongodb://' +
                           'master' + ':'
                           + 'YPULqbMZfLv3uipmKl4FHrQzo' + "@"
                       + 'ds053539.mongolab.com:53539/promuachat')


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"


RECAPTCHA_PUBLIC_KEY='6Le9UPgSAAAAAEyVicG0llU89xLaT5nCudwdk_to'
RECAPTCHA_PRIVATE_KEY='6Le9UPgSAAAAAA18fQ8_RWvHEJRUfgOAtk47phwb'
RECAPTCHA_USE_SSL =True
RECAPTCHA_OPTIONS = {'theme': 'clean'}