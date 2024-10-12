from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping({
            'SECRET_KEY': 'dev',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///store.db'
        })
    return app
