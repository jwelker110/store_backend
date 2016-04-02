from store_app.extensions import db, bcrypt
from datetime import datetime
from string import lower


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oa_id = db.Column(db.String(50), unique=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(250))
    confirmed_on = db.Column(db.DateTime)

    email = db.Column(db.String(250), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    username_lower = db.Column(db.String(20), nullable=False, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, oa_id=None, first_name=None,
                 last_name=None, email=None, username=None,
                 password=None, admin=False, confirmed=False):
        self.oa_id = oa_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.username_lower = lower(username)
        self.admin = admin
        self.confirmed = confirmed
        self.generate_password_hash(password)

    def __repr__(self):
        return "<User(%s)>" % self.username

    def generate_password_hash(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def dict(self):
        return {
            "username": self.username,
            "registered_on": self.registered_on.isoformat()
        }
