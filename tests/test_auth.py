import pytest


def test_login_success(client):
    resp = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert resp.status_code == 200
    assert 'access_token' in resp.get_json()


@pytest.mark.parametrize(
    'username, password, expected',
    [
        ('bad_user', 'admin123', 'Bad username or password'),
        ('admin', 'bad_password', 'Bad username or password')
    ]
)
def test_login_fail(client, username, password, expected):
    resp = client.post('/auth/login', json={
        'username': username,
        'password': password
    })
    assert resp.status_code == 401
    assert resp.get_json()['message'] == expected


def test_login_miss_field_fail(client):
    resp = client.post('/auth/login', json={
        'username': 'admin'
    })
    assert resp.status_code == 401
    assert resp.get_json()['message'] == 'Bad username or password'
