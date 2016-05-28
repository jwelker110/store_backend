from flask import Blueprint, request
from json import loads, dumps
from string import lower, replace
from sqlalchemy import desc
from werkzeug import secure_filename
from os import getcwd, remove

from store_app.database import Item
from store_app.extensions import db
from helpers import create_response, convertToInt, decode_jwt, allowed_filename, isNullOrUndefined

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/api/v1/items.json', methods=['GET', 'POST'])
def items_ep():
    if request.method == 'GET':

        offset = convertToInt(request.args.get('offset'))
        category = request.args.get('category')

        if category is None:
            items = Item.query.order_by(desc(Item.id)).offset(offset).limit(10).all()
        else:
            items = Item.query.order_by(desc(Item.id))\
                .filter_by(category=category).offset(offset).limit(10).all()

        return create_response({"items": items})

    elif request.method == 'POST':
        filename = 'uploads/common/placeholder.jpg'

        data = loads(request.data)

        # item info
        name = data.get('name')
        name = name.replace('+', ' ')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        sale_price = data.get('sale_price')
        stock = data.get('stock')

        # jwt to ensure user is authorized
        payload = decode_jwt(data.get('jwt_token'))

        if payload is None:
            return create_response({}, status=401)

        # make sure we have a name and price given
        if name is None or price is None:
            return create_response({}, status=400)

        # does the item already exist?
        item = Item.query.filter_by(name_lower=lower(name)).first()

        if item is not None:
            return create_response({}, status=400)

        try:

            item = Item(
                owner_name=payload.get('username'),
                name=name,
                description=None if isNullOrUndefined(description) else description,
                category=category,
                price=price,
                image_url=filename,
                sale_price=sale_price,
                stock=stock
            )
            db.session.add(item)
            db.session.commit()

            return create_response({})

        except:
            db.session.rollback()
            return create_response({}, status=500)


@item_bp.route('/api/v1/items/image', methods=['PUT'])
def item_image_ep():
    # if a file is given, we'll try to associate it with it's item
    # if the file is not accepted, we will leave the current file intact
    # if a file is not given (empty post), we will remove the current file
    # that is not the default and update our item with the default placeholder
    # image
    jwt_token = request.form.get('jwt_token')
    name = request.form.get('name')
    name = name.replace('+', ' ')

    image_file = request.files.get('image')

    payload = decode_jwt(jwt_token)
    if payload is None or isNullOrUndefined(name):
        return create_response({}, status=400)

    username = payload.get('username')

    # make sure the item exists
    item = Item.query.filter_by(name_lower=lower(name), owner_name=lower(username)).first()
    if item is None:
        return create_response({}, status=400)

    filename = 'uploads/common/placeholder.jpg'
    newFilename = None

    if image_file is not None:
        if allowed_filename(image_file.filename):
            try:
                ext = image_file.filename.split('.', 1)[1]
                print name.split(' ')
                print '_'.join(name.split(' '))
                name = '_'.join(name.split(' '))
                newFilename = 'uploads/' + secure_filename(name + '.' + ext)
                print newFilename
                f = open(getcwd() + '/' + newFilename, 'w')
                f.write(image_file.read())
                f.close()
            except:
                return create_response({}, status=500)
        else:
            return create_response({}, status=400)

    try:
        # get rid of existing file
        if item.image_url != filename:
                remove(getcwd() + '/' + item.image_url)

        item.image_url = filename if newFilename is None else newFilename

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
        name = name.replace('+', ' ')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')
        sale_price = data.get('sale_price')
        stock = data.get('stock')

        payload = decode_jwt(data.get('jwt_token'))

        if payload is None:
            return create_response({}, status=401)

        # get the item
        item = Item.query.filter_by(
            id=itemId, 
            owner_name=lower(payload.get('username'))).first()

        # does the item exist? how about the item meta?
        if item is None:
            return create_response({}, status=400)

        try:

            # everything checks out, update the item
            item.name = item.name if name is None else name
            item.description = item.description if description is None else description
            item.category = item.category if category is None else category
            item.price = item.price if price is None else price
            item.sale_price = item.sale_price if sale_price is None else sale_price
            item.stock = item.stock if stock is None else stock

            db.session.commit()

            return create_response({})

        except:
            db.session.rollback()
            return create_response({}, status=500)

