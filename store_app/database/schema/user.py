from datetime import datetime
from string import lower

from store_app.extensions import db


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oa_id = db.Column(db.String(50), unique=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    confirmed_on = db.Column(db.DateTime)

    email = db.Column(db.String(250), nullable=False, unique=True)
    email_lower = db.Column(db.String(250), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    username_lower = db.Column(db.String(20), nullable=False, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirm_secret = db.Column(db.String(15))
    confirm_secret_created_on = db.Column(db.DateTime)

    def __init__(self, oa_id=None, first_name=None,
                 last_name=None, email=None, username=None,
                 avatar_url=None, admin=False,
                 confirmed=False):
        self.oa_id = oa_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.email_lower = lower(email)
        self.username = username
        self.username_lower = lower(username)
        self.admin = admin
        self.confirmed = confirmed
        if self.confirmed:
            self.confirmed_on = datetime.now()

    def __repr__(self):
        return "<User(%s)>" % self.username

    def dict(self):
        return {
            "username": self.username,
            "registered_on": self.registered_on
        }
