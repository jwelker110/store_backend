from store_app.app import db
from database import User, Item, Category, CategoryItems


def create_test_data(app):
    with app.app_context():
        for i in range(1, 11):
            user = User(
                email="tester%s@email.com" % str(i),
                username="Tester%s" % str(i),
                confirmed=True
            )
            db.session.add(user)
        db.session.commit()
        for i in range(1, 6):
            cat = Category(
                name="Category%s" % str(i)
            )
            db.session.add(cat)
        db.session.commit()
        for i in range(1, 21):
            item = Item(
                name="Item%s" % str(i),
                description="This is item %s" % str(i),
                owner_name="Tester%s" % str(i),
                image_url="uploads/image.jpg",
                price=i*10.50,
                sale_price=i*8.75,
                stock=i,
            )
            db.session.add(item)
        db.session.commit()
