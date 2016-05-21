from flask import Blueprint, request
from json import loads
from string import lower
from sqlalchemy import desc

from store_app.database import Item
from store_app.extensions import db
from helpers import create_response, convertToInt, decode_jwt

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/api/v1/items.json', methods=['GET', 'POST'])
def items_ep():
    if request.method == 'GET':

        offset = convertToInt(request.args.get('offset'))
        category = request.args.get('category')

        if category is None:
            items = Item.query.order_by(desc(Item.id)).offset(offset).limit(10).all()
        else:
            items = db.session.query(Item).order_by(desc(Item.id))\
                .filter_by(category=category).offset(offset).limit(10).all()

        return create_response({"items": items})

    elif request.method == 'POST':

        data = loads(request.data)

        # item info
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        sale_price = data.get('sale_price')
        image_url = data.get('image_url')
        if image_url is None:
            image_url = 'uploads/image.jpg'
        stock = data.get('stock')

        # jwt to ensure user is authorized
        payload = decode_jwt(data.get('jwt_token'))

        if payload is None:
            return create_response({}, status=401)

        if payload.get('confirmed') is False:
            return create_response({}, status=401)

        if name is None or price is None:
            return create_response({}, status=400)

        try:

            item = Item(
                owner_name=lower(payload.get('username')),
                name=name,
                description=description,
                category=category,
                price=price,
                image_url=image_url,
                sale_price=sale_price,
                stock=stock
            )
            db.session.add(item)
            db.session.commit()

            return create_response({})

        except:
            db.session.rollback()
            return create_response({}, status=500)


@item_bp.route('/api/v1/items/details.json', methods=['GET', 'PUT', 'POST'])
def item_details_ep():
    if request.method == 'GET':

        name = request.args.get('name')
        if name is None:
            item = []
        else:
            item = Item.query.filter_by(name=name).first()
        # tuples are returned from the query so must be accessed via index
        return create_response({"item": item})

    elif request.method == 'POST':
        data = loads(request.data)
        payload = decode_jwt(data.get('jwt_token'))
        itemName = data.get('name')

        if payload is None:
            return create_response({}, status=401)

        item = Item.query.filter_by(
            name=itemName, 
            owner_name=lower(payload.get('username'))).first()

        if item is None:
            return create_response({}, status=400)

        try:
            db.session.delete(item)
            db.session.commit()
            return create_response({})
        except:        
            db.session.rollback()
            return create_response({}, status=500)

    elif request.method == 'PUT':

        data = loads(request.data)

        # item info
        itemId = data.get('id')
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        image_url = data.get('image_url')
        price = data.get('price')
        sale_price = data.get('sale_price')
        image_url = data.get('image_url')
        stock = data.get('stock')

        payload = decode_jwt(data.get('jwt_token'))

        if payload is None:
            return create_response({}, status=401)

        # get the item
        item = Item.query.filter_by(id=itemId).first()

        # does the item exist? how about the item meta?
        if item is None:
            return create_response({}, status=400)

        # does the user actually own the item?
        if item.owner_name != lower(payload.get('username')):
            # can't change someone else' item
            return create_response({}, status=401)

        try:

            # everything checks out, update the item
            item.name = item.name if name is None else name
            item.description = item.description if description is None else description
            item.category = item.category if category is None else category
            item.image_url = item.image_url if image_url is None else image_url
            item.price = item.price if price is None else price
            item.sale_price = item.sale_price if sale_price is None else sale_price
            item.image_url = item.image_url if image_url is None else image_url
            item.stock = item.stock if stock is None else stock

            db.session.commit()

            return create_response({})

        except:
            db.session.rollback()
            return create_response({}, status=500)

