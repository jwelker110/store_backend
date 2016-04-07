from flask import Blueprint, request
from string import lower
from jwt import encode, decode

from store_app.database import User, Item, Category
from helpers import create_response, convertToInt

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/api/v1/users.json', methods=['GET', 'POST'])
def users_ep():
    if request.method == 'GET':
        offset = convertToInt(request.args.get('offset'))
        users = User.query.offset(offset).limit(25).all()

        return create_response({"users": users})

    elif request.method == 'POST':
        # create a new user
        return "POSTED"


@user_bp.route('/api/v1/users/items.json', methods=['GET', 'POST'])
def usersItems_ep():
    if request.method == 'GET':
        offset = convertToInt(request.args.get('offset'))
        username = request.args.get('username')

        if username is None:
            items = []
        else:
            items = Item.query.filter_by(owner_name=lower(username)).offset(offset).limit(25).all()

        return create_response({"items": items})
    elif request.method == 'POST':
        # create an item associated with the logged in user
        return 'POSTED'
