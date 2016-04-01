from flask import Blueprint

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/users', methods=['GET'])
def users():
    return "Users"


@user_bp.route('/users/<int:offset>', methods=['GET'])
def usersByOffset(offset):
    return "The offset is: %s" % offset


@user_bp.route('/user/<string:username>', methods=['GET'])
def userByUsername(username):
    return "The username is: %s" % username


@user_bp.route('/user/<string:username>/items', methods=['GET'])
def itemsByUsername(username):
    return "The username is: %s" % username


@user_bp.route('/user/<string:username>/items/<int:offset>', methods=['GET'])
def itemsByUsernameOffset(username, offset):
    return "The username is: %s and the offset is: %s" % (username, offset)

@user_bp.route('/user', methods=['POST'])
def user():
    pass
