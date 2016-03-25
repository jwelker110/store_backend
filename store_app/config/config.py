import os

_absolute_path = os.path.dirname(os.path.abspath(__file__))
_config_path = os.path.join(_absolute_path, 'config_secret.json')


class BaseConfig(object):
    PROJECT = 'Store App'
    PROJECT_ROOT = _absolute_path
    STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')
    TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')
    UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'uploads')

    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
