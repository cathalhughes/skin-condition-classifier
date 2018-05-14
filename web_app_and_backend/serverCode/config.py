
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'skinconditionclassifier@gmail.com'
MAIL_PASSWORD = '3rdyearproject'
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['skinconditionclassifier@gmail.com']

class TestConfig():
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False