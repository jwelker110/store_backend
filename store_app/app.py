from flask import Flask
from extensions import db, mail, bcrypt
from config import DevelopmentConfig
from database import User, Category, Item

DEFAULT_BLUEPRINTS = ()


def create_app(app_name=__name__, blueprints=DEFAULT_BLUEPRINTS, config=DevelopmentConfig):
    # create and set up the application
    app = Flask(app_name)
    app.config.from_object(DevelopmentConfig)
    app.config.from_pyfile('config_secret.py')
    configure_extensions(app)

    return app


def configure_processors(app):

    @app.after_request
    def after_request(response):
        # TODO would be changed in prod
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        return response

    @app.error_handler(404)
    def error_handler(error):
        pass


def configure_extensions(app):
    # setup SQLAlchemy
    db.init_app(app)
    db.create_all(app=app)

    mail.init_app(app)

    bcrypt.init_app(app)


def configure_blueprints(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)
