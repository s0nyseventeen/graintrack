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
