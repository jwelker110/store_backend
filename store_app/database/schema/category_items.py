from store_app.extensions import db


class CategoryItems(db.Model):
    __tablename__ = 'Category_Items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)

    db.ForeignKeyConstraint(['category_id', 'item_id'], ['category.id', 'item.id'])
