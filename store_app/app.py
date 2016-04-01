from flask import Flask
from extensions import db, mail, bcrypt
from config import DevelopmentConfig
from blueprints import user_bp, item_bp, category_bp

DEFAULT_BLUEPRINTS = (user_bp,)


def create_app(app_name='Store App', blueprints=DEFAULT_BLUEPRINTS, config=DevelopmentConfig):
    # create and set up the application
    app = Flask(app_name)

    app.config.from_object(config)
    app.config.from_pyfile(app.config['CONFIG_PATH'])
    configure_extensions(app)
    configure_processors(app)
    configure_blueprints(app, blueprints)

    return app


def configure_processors(app):

    @app.after_request
    def after_request(response):
        # TODO would be changed in prod
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        return response

    @app.errorhandler(404)
    def error_handler(error):
        return 'Error', 404

    @app.route('/')
    def index():
        return 'hello world'


def configure_extensions(app):
    # setup SQLAlchemy
    db.init_app(app)
    db.create_all(app=app)

    mail.init_app(app)

    bcrypt.init_app(app)


def configure_blueprints(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)
