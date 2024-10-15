from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required

from src import db
from src.models import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/create', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    if not data:
        abort(
            400,
            description='Required fields: "name", "price", "amount", "category_id"'
        )

    new_product = Product(
        name=data['name'],
        price=data['price'],
        amount=data.get('amount', 1),
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201


@bp.route('/all', methods=['GET'])
def get_all():
    products = Product.query.filter(Product.amount > 0).all()
    return jsonify([product.to_dict() for product in products]), 200


@bp.route('/update/<int:product_id>', methods=['PATCH'])
@jwt_required()
def update_price(product_id):
    data = request.get_json()
    if not data:
        abort(400, description='Required field: "price"')
        
    product = Product.query.get_or_404(product_id)
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Price was changed successfully'}), 204


@bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product was deleted successfully'}), 204


@bp.route('/filter', methods=['GET'])
def filter_products():
    category_id = request.args.get('category_id', type=int)
    if not category_id:
        return jsonify({'message': 'Category is not provided'})

    products = Product.query.filter(Product.amount > 0).filter_by(category_id=category_id).all()
    return jsonify([product.to_dict() for product in products]), 200


@bp.route('/<int:product_id>/set_discount', methods=['PATCH'])
@jwt_required()
def set_discount(product_id):
    data = request.get_json()
    if not data:
        abort(400, description='Required field: "discount"')

    product = Product.query.get_or_404(product_id)
    discount = data['discount']
    if not (0 < discount < 100):
        abort(400, description='Discount must be between 0 and 100')

    product.discount = discount
    db.session.commit()
    return jsonify({
        'message': f'{discount=}% was set',
        'product': product.to_dict()
    }), 200


@bp.route('/<int:product_id>/reserve', methods=['PATCH'])
def reserve(product_id):
    product = Product.query.get_or_404(product_id)
    if product.reserved:
        return jsonify({'message': 'Product is already reserved'}), 400

    if product.amount <= 0:
        return jsonify({'message': 'Product is out of stock'}), 400

    product.amount -= 1
    product.reserved = True
    db.session.commit()
    return jsonify({
        'message': 'Product reserved successfully',
        'product': product.to_dict()
    }), 200


@bp.route('/<int:product_id>/unreserve', methods=['PATCH'])
def unreserve(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.reserved:
        return jsonify({'message': 'Product is not reserved'}), 400

    product.reserved = False
    product.amount += 1
    db.session.commit()
    return jsonify({
        'message': 'Product unreserved successfully',
        'product': product.to_dict()
    }), 200


@bp.route('/<int:product_id>/sell', methods=['PATCH'])
def sell(product_id):
    product = Product.query.get_or_404(product_id)
    if product.sold:
        return jsonify({'message': 'Product has already been sold'}), 400

    if product.amount <= 0:
        return jsonify({'message': 'Product is out of stock'}), 400

    product.reserved = False
    product.sold = True
    product.amount -= 1
    db.session.commit()
    return jsonify({
        'message': 'Product sold successfully',
        'product': product.to_dict()
    }), 200


@bp.route('/report', methods=['GET'])
@jwt_required()
def sold_report():
    category_id = request.args.get('category_id', type=int)
    query = Product.query.filter_by(sold=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    sold = query.all()
    return jsonify([product.to_dict() for product in sold]), 200
