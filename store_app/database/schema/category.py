from string import lower

from store_app.extensions import db


class Category(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name_lower = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name='Other'):
        self.name = name
        self.name_lower = lower(name)

    def __repr__(self):
        return "<Category(%s)>" % self.name

    def dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
