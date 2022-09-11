import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI ="postgresql://exstpgzbdtihxw:238a582c9b444a62f503fee859b5030bb119d8c84dc19abf8259830ddf2321cd@ec2-3-214-2-141.compute-1.amazonaws.com:5432/dkomrrdnof95n"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

