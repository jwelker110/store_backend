from flask import Blueprint, request
from json import loads
from string import lower

from store_app.database import Item, ItemMeta, CategoryItems, Category
from store_app.extensions import db
from helpers import create_response, convertToInt, decode_jwt

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/api/v1/items.json', methods=['GET', 'POST'])
def items_ep():

    if request.method == 'GET':

        offset = convertToInt(request.args.get('offset'))
        category = request.args.get('category')

        if category is None:
            items = Item.query.offset(offset).limit(25).all()
        else:
            items = db.session.query(Item)\
                .outerjoin(CategoryItems)\
                .outerjoin(Category)\
                .filter_by(name=category).offset(offset).limit(25).all()

        return create_response({"items": items})

    elif request.method == 'POST':

        data = loads(request.data)

        # item info
        name = data.get('name')
        description = data.get('description')

        # meta info
        price = data.get('price')
        image_url = data.get('image_url')
        sale_price = data.get('sale_price')
        stock = data.get('stock')
        meta_description = data.get('meta_description')
        meta_key = data.get('meta_key')
        meta_value = data.get('meta_value')

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
                description=description
            )
            db.session.add(item)
            db.session.commit()

            item_meta = ItemMeta(
                item_id=item.id,
                price=price,
                image_url=image_url,
                sale_price=sale_price,
                stock=stock,
                description=meta_description,
                meta_key=meta_key,
                meta_value=meta_value
            )
            db.session.add(item_meta)
            db.session.commit()
            return create_response({})

        except:
            return create_response({}, status=500)


@item_bp.route('/api/v1/items/details.json', methods=['GET', 'PUT'])
def item_details_ep():

    if request.method == 'GET':

        name = request.args.get('name')
        if name is None:
            item = []
        else:
            item = db.session.query(Item, ItemMeta).filter_by(name=name).outerjoin(ItemMeta).all()
        return create_response({"items": [item[0][0]] if len(item) > 0 else [],
                                "item_meta": [i[1] for i in item]})

    elif request.method == 'PUT':

        data = loads(request.data)

        # item info
        name = data.get('name')
        description = data.get('description')

        # meta info
        id = data.get('id')
        price = data.get('price')
        sale_price = data.get('sale_price')
        stock = data.get('stock')
        meta_description = data.get('meta_description')
        meta_key = data.get('meta_key')
        meta_value = data.get('meta_value')

        payload = decode_jwt(data.get('jwt_token'))

        if payload is None:
            return create_response({}, status=401)

        # get the item
        item = Item.query.filter(name=name).first()

        # get the item meta
        item_meta = ItemMeta.query.filter(id=id).first()

        # does the item exist? how about the item meta?
        if item is None or item_meta is None:
            return create_response({}, status=400)

        # does the item meta belong to the item?
        if item_meta.item_id != item.id:
            return create_response({}, status=400)

        # does the user actually own the item?
        if item.owner_name != lower(payload.get('username')):
            # can't change someone else' item
            return create_response({}, status=401)

        try:

            # everything checks out, update the item
            item.name = item.name if name is None else name
            item.description = item.description if description is None else description

            db.session.commit()

            # the item has been updated, update the meta
            item_meta.price = item_meta.price if price is None else price
            item_meta.sale_price = item_meta.sale_price if sale_price is None else sale_price
            item_meta.stock = item_meta.stock if stock is None else stock
            item_meta.meta_description = item_meta.meta_description if meta_description is None else meta_description
            item_meta.meta_key = item_meta.meta_key if meta_key is None else meta_key
            item_meta.meta_value = item_meta.meta_value if meta_value is None else meta_value

            db.session.commit()

            return create_response({})

        except:
            return create_response({}, status=500)

