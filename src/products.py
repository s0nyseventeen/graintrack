from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

from src import db
from src.models import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/create', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        abort(400, description='Required fields: "name", "price", "category_id"')

    new_product = Product(
        name=data['name'], price=data['price'], category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201


@bp.route('/all', methods=['GET'])
def get_all():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])
