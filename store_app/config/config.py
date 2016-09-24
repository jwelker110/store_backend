import os

_absolute_path = os.path.dirname(os.path.abspath(__file__))
_config_path = os.path.join(_absolute_path, 'config_secret.py')
_secret_key_path = os.path.join(_absolute_path, 'secret_keys.json')


class BaseConfig(object):
    PROJECT = 'Store App'
    PROJECT_ROOT = _absolute_path
    STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')
    TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')
    UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'uploads')
    CONFIG_PATH = _config_path
    SECRET_KEY_PATH = _secret_key_path
    MAX_CONTENT_LENGTH = (1024 ** 2) / 2

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):  # todo change to postgres pls
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://catalog:catalog@localhost/catalogdb'
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    DEBUG = True
    TESTING = True
