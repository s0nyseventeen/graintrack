import pytest

from src import db
from src.models import Product


@pytest.fixture
def create_prod(app):

    def get_prod_id(
        name, price, category_id, sold=False, reserved=False, discount=0.0
    ):
        prod = Product(
            name=name,
            price=price,
            category_id=category_id,
            sold=sold,
            reserved=reserved,
            discount=discount
        )
        with app.app_context():
            db.session.add(prod)
            db.session.commit()
            prod_id = prod.id
        return prod_id

    return get_prod_id


def test_create_product(client):
    new_prod = {
        'name': 'Test Product',
        'price': 10.0,
        'category_id': 1
    }
    resp = client.post('/products/create', json=new_prod)

    assert resp.status_code == 201
    prod_data = resp.get_json()
    assert prod_data['name'] == new_prod['name']
    assert prod_data['price'] == new_prod['price']
    assert prod_data['category_id'] == new_prod['category_id']


def test_get_all(client, create_prod):
    create_prod('Product1', 10.0, 1)
    create_prod('Product2', 20.0, 2)

    resp = client.get('/products/all')
    assert resp.status_code == 200
    products = resp.get_json()
    assert len(products) == 2
    assert all(
        prod['name'] == f'Product{i+1}' for i, prod in enumerate(products)
    )


def test_update_price(app, client, create_prod):
    prod_id = create_prod('Product1', 20.0, 1)
    resp = client.patch(f'/products/{prod_id}', json={'price': 25.0})
    assert resp.status_code == 204
    
    with app.app_context():
        updated_prod = db.session.get(Product, prod_id)
        assert updated_prod.price == 25.0


def test_delete_product(app, client, create_prod):
    prod_id = create_prod('Product1', 10.0, 1)
    resp = client.delete(f'/products/{prod_id}')
    assert resp.status_code == 204
    
    with app.app_context():
        deleted_prod = db.session.get(Product, prod_id)
        assert deleted_prod is None
