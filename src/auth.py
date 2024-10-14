from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username != 'admin' or password != 'admin123':
        return jsonify({'message': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
