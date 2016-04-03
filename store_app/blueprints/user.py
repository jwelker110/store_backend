from flask import Blueprint
from string import lower

from store_app.database import User, Item, Category
from helpers import Resp, simple_enc

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/users', methods=['GET'])
def getUsers():
    users = User.query.limit(10)
    return Resp(simple_enc("users", users))


@user_bp.route('/users/<int:offset>', methods=['GET'])
def getUsersByOffset(offset):
    users = User.query.offset(offset).limit(10)
    return Resp(simple_enc("users", users))


@user_bp.route('/user/<string:username>', methods=['GET'])
def getUserByUsername(username):
    user = User.query.filter_by(username_lower=lower(username)).limit(10)
    return Resp(simple_enc("users", user))


@user_bp.route('/user/<string:username>/items', methods=['GET'])
def getItemsByUsername(username):
    items = Item.query.filter_by(owner_name=lower(username)).limit(10)
    return Resp(simple_enc("items", items))


@user_bp.route('/user/<string:username>/items/<int:offset>', methods=['GET'])
def getItemsByUsernameOffset(username, offset):
    items = Item.query.filter_by(owner_name=lower(username)).offset(offset).limit(10)
    return Resp(simple_enc("items", items))


@user_bp.route('/user', methods=['POST'])
def postUser():
    pass
