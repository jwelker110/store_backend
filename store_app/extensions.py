from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.make_declarative_base()