from flask import Blueprint

from store_app.database import Item, ItemMeta
from store_app.extensions import db
from helpers import create_response

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/items', methods=['GET'])
def getItems():
    items = Item.query.limit(10).all()
    return create_response({"items": items})


@item_bp.route('/items/<int:offset>', methods=['GET'])
def getItemsByOffset(offset):
    items = Item.query.offset(offset).limit(10).all()
    return create_response({"items": items})


@item_bp.route('/item/<string:itemName>', methods=['GET'])
def getItemByName(itemName):
    item = db.session.query(Item, ItemMeta).filter_by(name=itemName).outerjoin(ItemMeta).all()
    for i in item:
        print i
    return create_response({"item": item[0][0] if len(item) > 0 else [],
                            "item_meta": [i[1] for i in item]})


@item_bp.route('/item', methods=['POST'])
def postItem():
    pass
