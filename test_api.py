from app import app
import pytest

# Fixture to configure the test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_info_success_known_ip(client):
    """Tests the endpoint with a well-known, valid IP."""
    response = client.get('/get_info?ip=8.8.8.8')
    data = response.get_json()

    assert response.status_code == 200
    assert data is not None
    assert data.get('IP Address') == '8.8.8.8'
    assert data.get('Organization') == 'GOOGLE'
    assert 'error' not in data

def test_get_info_no_ip_success(client):
    """Tests the endpoint when no IP is provided (relies on external ipify call)."""
    response = client.get('/get_info')
    data = response.get_json()

    # We can't know the exact IP, but we assert structure and success
    assert response.status_code == 200
    assert data is not None
    assert 'IP Address' in data
    assert 'Organization' in data

def test_get_info_invalid_ip_failure(client):
    """Tests Example Feature 1: Validation with bad input."""
    response = client.get('/get_info?ip=notanip')
    data = response.get_json()

    # The API should return a 400 Bad Request if the input validation fails
    assert response.status_code == 400
    assert data is not None
    assert 'error' in data
    assert 'Invalid IP address format.' in data.get('error')

def test_index_page_loads(client):
    """Tests that the root URL loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
