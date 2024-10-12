from pytest import fixture

from src import create_app
from src import db


@fixture
def app():
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'dev',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@fixture
def client(app):
    return app.test_client()
