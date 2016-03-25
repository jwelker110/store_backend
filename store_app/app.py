from flask import Flask
from extensions import db

DEFAULT_BLUEPRINTS = ()


def create_app(app_name=__name__, blueprints=DEFAULT_BLUEPRINTS, config=DevelopmentConfig):
    # create and set up the application
    app = Flask(app_name)
    app.config.from_object(config)
    configure_extensions(app)

    return app


def configure_extensions(app):
    # setup SQLAlchemy
    db.init_app(app)