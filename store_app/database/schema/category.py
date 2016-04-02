from store_app.extensions import db


class Category(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Category(%s)>" % self.name

    def dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
