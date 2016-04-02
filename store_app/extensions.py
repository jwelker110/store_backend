from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.make_declarative_base()

from flask_mail import Mail
mail = Mail()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()