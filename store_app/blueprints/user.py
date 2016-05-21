from flask import Blueprint, request
from string import lower
from jwt import encode, decode
from sqlalchemy import desc

from store_app.database import User, Item, Category
from helpers import create_response, convertToInt

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/api/v1/users.json', methods=['GET'])
def users_ep():
    offset = convertToInt(request.args.get('offset'))
    users = User.query.offset(offset).limit(20).all()

    return create_response({"users": users})


@user_bp.route('/api/v1/users/items.json', methods=['GET'])
def users_items_ep():
    offset = convertToInt(request.args.get('offset'))
    username = request.args.get('username')

    if username is None:
        items = []
    else:
        items = Item.query.filter_by(owner_name=lower(username)).order_by(desc(Item.id)).offset(offset).limit(20).all()

    return create_response({"items": items})


@user_bp.route('/api/v1/users/exists.json', methods=['GET'])
def users_exists_ep():
    username = request.args.get('username')

    if username is None:
        return create_response({}, status=400)

    user = User.query.filter_by(username_lower=lower(username)).first()
    if user is None:
        return create_response({"exists": False})

    return create_response({"exists": True})
