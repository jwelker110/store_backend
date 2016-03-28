import os

_absolute_path = os.path.dirname(os.path.abspath(__file__))
_config_path = os.path.join(_absolute_path, 'config_secret.py')


class BaseConfig(object):
    PROJECT = 'Store App'
    PROJECT_ROOT = _absolute_path
    STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')
    TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')
    UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'uploads')
    CONFIG_PATH = _config_path

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    DEBUG = True
    TESTING = True
