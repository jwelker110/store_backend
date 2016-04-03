from flask import Blueprint

from store_app.database import Item, ItemMeta
from store_app.extensions import db
from helpers import create_response

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/items', methods=['GET'])
def getItems():
    items = Item.query.limit(10)
    return create_response({"items": items})


@item_bp.route('/items/<int:offset>', methods=['GET'])
def getItemsByOffset(offset):
    items = Item.query.offset(offset).limit(10)
    return create_response({"items": items})


@item_bp.route('/item/<string:itemName>', methods=['GET'])
def getItemByName(itemName):
    item = db.session.query(ItemMeta, Item).outerjoin(Item).filter_by(name=itemName)
    return create_response({"item": item[0][1], "item_meta": [i[0] for i in item]})


@item_bp.route('/item', methods=['POST'])
def postItem():
    pass
