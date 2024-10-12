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


@bp.route('/<int:product_id>', methods=['PATCH'])
def update_price(product_id):
    data = request.get_json()
    if not data:
        abort(400, description='Required field: "price"')
        
    product = Product.query.get_or_404(product_id)
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Price was changed successfully'}), 204


@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product was deleted successfully'}), 204
