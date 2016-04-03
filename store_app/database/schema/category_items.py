from store_app.extensions import db


class CategoryItems(db.Model):
    __tablename__ = 'Category_Items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("Category.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable=False)

    db.ForeignKeyConstraint(['category_id', 'item_id'], ['category.id', 'item.id'])

    def __init__(self, category_id, item_id):
        self.category_id = category_id
        self.item_id = item_id

    def __repr__(self):
        return "<CategoryItem(category_id: %s, item_id: %s>" % (self.category_id, self.item_id)

    def dict(self):
        return {
            "category_id": self.category_id,
            "item_id": self.item_id
        }
