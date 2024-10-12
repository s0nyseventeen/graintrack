from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping({
            'SECRET_KEY': 'dev',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///store.db'
        })

    db.init_app(app)
    migrate = Migrate(app, db)
    return app
