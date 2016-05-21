from datetime import datetime
from store_app.extensions import db
from string import lower


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50), db.ForeignKey("Category.name"), nullable=False)
    owner_name = db.Column(db.String(20), db.ForeignKey("User.username_lower"), nullable=False)
    image_url = db.Column(db.String(25))
    price = db.Column(db.Numeric, nullable=False)
    sale_price = db.Column(db.Numeric)
    stock = db.Column(db.Integer)
    created_on = db.Column(db.DateTime)

    def __init__(self, owner_name, name=None, description=None, category="Other", image_url=None, price=None, sale_price=None, stock=None):
        self.name = name
        self.description = description
        self.category = category
        self.owner_name = lower(owner_name)
        self.image_url = image_url
        self.price = price
        self.sale_price = sale_price
        self.stock = stock
        self.created_on = datetime.now()

    # def __repr__(self):
    #     return "<Item(%s)>" % self.name

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "owner_name": self.owner_name,
            "image_url": self.image_url,
            "price": self.price,
            "sale_price": self.sale_price,
            "stock": self.stock,
            "created_on": self.created_on
        }

