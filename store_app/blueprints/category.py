from flask import Blueprint

from store_app.database import Category
from helpers import create_response

category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/api/v1/categories.json', methods=['GET'])
def categories_ep():
    cats = Category.query.all()
    return create_response({"categories": cats})
