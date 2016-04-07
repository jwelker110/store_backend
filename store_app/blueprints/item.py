from flask import Blueprint, request

from store_app.database import Item, ItemMeta, CategoryItems, Category
from store_app.extensions import db
from helpers import create_response, convertToInt

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/api/v1/items.json', methods=['GET', 'POST'])
def items_ep():
    if request.method == 'GET':
        offset = convertToInt(request.args.get('offset'))
        category = request.args.get('category')

        if category is None:
            items = Item.query.offset(offset).limit(25).all()
        else:
            items = db.session.query(Item)\
                .outerjoin(CategoryItems)\
                .outerjoin(Category)\
                .filter_by(name=category).offset(offset).limit(25).all()

        return create_response({"items": items})

    elif request.method == 'POST':
        # create item here or in the users blueprint?
        return "POSTED"


@item_bp.route('/api/v1/items/details.json', methods=['GET', 'PUT'])
def itemDetails_ep():
    if request.method == 'GET':
        name = request.args.get('name')
        if name is None:
            item = []
        else:
            item = db.session.query(Item, ItemMeta).filter_by(name=name).outerjoin(ItemMeta).all()
        return create_response({"item": item[0][0] if len(item) > 0 else [],
                                "item_meta": [i[1] for i in item]})
    elif request.method == 'PUT':
        # update the item details
        return "PUT'"

