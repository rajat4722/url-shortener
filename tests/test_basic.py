import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "healthy"

def test_shorten_invalid_url(client):
    rv = client.post('/api/shorten', json={"url": "not_a_url"})
    assert rv.status_code == 400

def test_shorten_and_redirect(client):
    rv = client.post('/api/shorten', json={"url": "http://example.com"})
    assert rv.status_code == 201
    data = rv.get_json()
    short_code = data["short_code"]

    # Test redirect
    rv2 = client.get(f'/{short_code}', follow_redirects=False)
    assert rv2.status_code == 302
    assert rv2.headers["Location"] == "http://example.com"

def test_stats(client):
    rv = client.post('/api/shorten', json={"url": "http://example.org"})
    short_code = rv.get_json()["short_code"]
    client.get(f'/{short_code}')
    rv2 = client.get(f'/api/stats/{short_code}')
    data = rv2.get_json()
    assert data["original_url"] == "http://example.org"
    assert data["clicks"] == 1

def test_stats_not_found(client):
    rv = client.get('/api/stats/unknown')
    assert rv.status_code == 404