from flask import Flask
from json import loads
from extensions import db
from config import ProductionConfig
from blueprints import user_bp, item_bp, category_bp, auth_bp
from blueprints.helpers import create_response

import os

DEFAULT_BLUEPRINTS = (user_bp, item_bp, category_bp, auth_bp)


def create_app(app_name='Store App', blueprints=DEFAULT_BLUEPRINTS, config=ProductionConfig):
    # create and set up the application
    app = Flask(app_name)

    app.config.from_object(config)
    app.config.from_pyfile(app.config['CONFIG_PATH'])
    configure_extensions(app)
    configure_processors(app)
    configure_blueprints(app, blueprints)
    configure_env(app)

    return app


def configure_processors(app):

    @app.after_request
    def after_request(response):
        # TODO would be changed in prod
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Content-Type', 'application/json')
        return response

    @app.errorhandler(404)
    def error_handler(error):
        return create_response({}, status=404)


def configure_extensions(app):
    # setup SQLAlchemy
    db.init_app(app)
#    db.drop_all(app=app)
    db.create_all(app=app)
#    from dummy_data import create_test_data
#    create_test_data(app)


def configure_blueprints(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)


def configure_env(app):
    secret_key_path = app.config.get('SECRET_KEY_PATH')
    if secret_key_path is None:
        return
    # set up the environment vars
    secrets = loads(open(secret_key_path).read())
    for key, value in secrets.iteritems():
        os.environ[key] = value
