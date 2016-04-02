from datetime import datetime
from store_app.extensions import db


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500))
    owner_name = db.Column(db.String(20), db.ForeignKey("User.username_lower"), nullable=False)

    def __repr__(self):
        return "<Item(%s)>" % self.name

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_name": self.owner_name
        }


class ItemMeta(db.Model):
    __tablename__ = "Item_Meta"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    sale_price = db.Column(db.Numeric, nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    description = db.Column(db.String(120))
    meta_key = db.Column(db.String(20))
    meta_value = db.Column(db.String(20))

    def dict(self):
        return {
            "price": self.price,
            "sale_price": self.sale_price,
            "stock": self.stock,
            "created_on": self.created_on,
            "description": self.description,
            "meta_key": self.meta_key,
            "meta_value": self.meta_value
        }
