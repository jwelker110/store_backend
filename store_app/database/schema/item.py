from datetime import datetime
from store_app.extensions import db


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric, nullable=False)
    sale_price = db.Column(db.Numeric, nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    creator_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("Category.id"))

    # create the Item.creator relationship, which also creates the User.items
    # relationship which holds a collection of items for each user
    creator = db.relationship("User", backref="items")
    # create the Item.category relationship, which also creates the Category.items
    # relationship which holds a collection of items for each user
    category = db.relationship("Category", backref="items")

    def __repr__(self):
        return "<Item(%s)>" % self.name
