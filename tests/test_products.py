import pytest

from src import db
from src.models import Category
from src.models import Product


@pytest.fixture
def create_prod(app):

    def get_prod_id(
        name,
        price,
        category_id,
        amount=1,
        sold=False,
        reserved=False,
        discount=0.0
    ):
        prod = Product(
            name=name,
            price=price,
            category_id=category_id,
            amount=amount,
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


@pytest.fixture
def create_category(app):

    def get_category_id(name='Test Category'):
        category = Category(name=name)
        with app.app_context():
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        return category_id

    return get_category_id


@pytest.fixture
def jwt_token(client):
    data = {'username': 'admin', 'password': 'admin123'}
    resp = client.post('/auth/login', json=data)
    return resp.get_json()['access_token']


def test_create_product(client, jwt_token):
    new_prod = {
        'name': 'Test Product',
        'price': 10.0,
        'category_id': 1
    }
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.post('/products/create', json=new_prod, headers=headers)

    assert resp.status_code == 201
    prod_data = resp.get_json()
    assert prod_data['name'] == new_prod['name']
    assert prod_data['price'] == new_prod['price']
    assert prod_data['category_id'] == new_prod['category_id']


def test_get_all(client, create_prod):
    create_prod('Product1', 10.0, 1, amount=5)
    create_prod('Product2', 20.0, 2, amount=3)

    resp = client.get('/products/all')
    assert resp.status_code == 200
    products = resp.get_json()
    assert len(products) == 2
    assert all(
        prod['name'] == f'Product{i+1}' for i, prod in enumerate(products)
    )


def test_update_price(app, client, create_prod, jwt_token):
    prod_id = create_prod('Product1', 20.0, 1)
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.patch(
        f'/products/update/{prod_id}', json={'price': 25.0}, headers=headers
    )
    assert resp.status_code == 204
    
    with app.app_context():
        updated_prod = db.session.get(Product, prod_id)
        assert updated_prod.price == 25.0


def test_delete_product(app, client, create_prod, jwt_token):
    prod_id = create_prod('Product1', 10.0, 1)
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.delete(f'/products/{prod_id}', headers=headers)
    assert resp.status_code == 204
    
    with app.app_context():
        deleted_prod = db.session.get(Product, prod_id)
        assert deleted_prod is None


def test_filter_products(client, create_prod):
    create_prod('Product1', 10.0, 1)
    create_prod('Product2', 20.0, 2)

    resp = client.get('/products/filter?category_id=1')
    assert resp.status_code == 200
    products = resp.get_json()
    assert len(products) == 1
    assert products[0]['category_id'] == 1


def test_set_discount_success(client, create_prod, jwt_token):
    prod_id = create_prod('Test Product', 10.0, 1)
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.patch(
        f'/products/{prod_id}/set_discount',
        json={'discount': 25.0},
        headers=headers
    )
    assert resp.status_code == 200
    assert resp.get_json()['product']['discount'] == 25.0


@pytest.mark.parametrize(
    'discount, status_code', [(150.0, 400), (0, 400)]
)
def test_set_discount_fail(client, create_prod, jwt_token, discount, status_code):
    prod_id = create_prod('Test Product', 10.0, 1)
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.patch(
        f'/products/{prod_id}/set_discount', json={'discount': discount}, headers=headers
    )
    assert resp.status_code == status_code


def test_reserve_success(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1, amount=5)
    resp = client.patch(f'/products/{prod_id}/reserve')
    assert resp.status_code == 200
    product = resp.get_json()['product']
    assert resp.get_json()['message'] == 'Product reserved successfully'
    assert product['reserved']
    assert product['amount'] == 4


def test_reserve_no_amount(client, create_prod):
    prod_id = create_prod('Test Product out of stock', 10.0, 1, amount=0)
    resp = client.patch(f'/products/{prod_id}/reserve')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Product is out of stock'


def test_reserve_already_reserved(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1, reserved=True)
    resp = client.patch(f'/products/{prod_id}/reserve')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Product is already reserved'


def test_unreserve_success(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1, amount=4, reserved=True)
    resp = client.patch(f'/products/{prod_id}/unreserve')
    assert resp.status_code == 200
    product = resp.get_json()['product']
    assert resp.get_json()['message'] == 'Product unreserved successfully'
    assert not product['reserved']
    assert product['amount'] == 5


def test_unreserve_not_reserved(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1)
    resp = client.patch(f'/products/{prod_id}/unreserve')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Product is not reserved'


def test_sell_success(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1)
    resp = client.patch(f'/products/{prod_id}/sell')
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Product sold successfully'
    assert resp.get_json()['product']['sold']


def test_sell_already_sold(client, create_prod):
    prod_id = create_prod('Test Product', 20.0, 1, sold=True)
    resp = client.patch(f'/products/{prod_id}/sell')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Product has already been sold'


def test_sold_report_without_filtering_category(
    client, create_category, create_prod, jwt_token
):
    category_id = create_category()
    create_prod('Sold Product 1', 10.0, category_id, sold=True)
    create_prod('Sold Product 2', 20.0, category_id, sold=True)

    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.get('/products/report', headers=headers)
    assert resp.status_code == 200
    sold_products = resp.get_json()
    assert len(sold_products) == 2


def test_sold_report_with_filtering_category(
    client, create_category, create_prod, jwt_token
):
    category_id = create_category()
    create_prod('Sold Product 1', 10.0, category_id, sold=True)
    create_prod('Sold Product 2', 20.0, category_id, sold=True)

    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = client.get(
        f'/products/report?category_id={category_id}', headers=headers
    )
    assert resp.status_code == 200
    sold_products = resp.get_json()
    assert len(sold_products) == 2
    assert all(prod['category_id'] == category_id for prod in sold_products)
