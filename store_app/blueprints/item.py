from flask import Blueprint

from store_app.database import Item, ItemMeta
from store_app.extensions import db
from helpers import Resp, simple_enc, multi_enc

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/items', methods=['GET'])
def getItems():
    items = Item.query.limit(10)
    return Resp(simple_enc("items", items))


@item_bp.route('/items/<int:offset>', methods=['GET'])
def getItemsByOffset(offset):
    items = Item.query.offset(offset).limit(10)
    return Resp(simple_enc("items", items))


@item_bp.route('/item/<string:itemName>', methods=['GET'])
def getItemByName(itemName):
    item = db.session.query(Item, ItemMeta).filter_by(name=itemName).outerjoin(ItemMeta)
    return Resp(multi_enc({"item": [item[0][0]], "meta": [item[0][1]]}))


@item_bp.route('/item', methods=['POST'])
def postItem():
    pass
