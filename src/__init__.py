from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping({
            'SECRET_KEY': 'dev',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///store.db',
            'JWT_SECRET_KEY': 'dev_jwt_secret_key'
        })

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    from . import products
    app.register_blueprint(products.bp)

    return app
