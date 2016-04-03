from flask import Blueprint

from store_app.database import Category, Item, User, CategoryItems
from helpers import Resp, simple_enc
from store_app.extensions import db

category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories', methods=['GET'])
def getCategories():
    cats = Category.query.all()
    return Resp(simple_enc("categories", cats))


@category_bp.route('/category/<string:category>/items')
def getItemsByCategory(category):
    items = db.session.query(Item).outerjoin(CategoryItems).outerjoin(Category).filter_by(name=category).limit(10)
    return Resp(simple_enc("items", items))


@category_bp.route('/category/<string:category>/items/<int:offset>')
def getItemsByCategoryOffset(category, offset):
    items = db.session.query(Item).outerjoin(CategoryItems).outerjoin(Category).filter_by(name=category).offset(offset).limit(10)
    return Resp(simple_enc("items", items))
