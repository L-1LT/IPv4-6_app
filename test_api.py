from app import app

def test_app_running():
    test_client = app.test_client()
    response = test_client.get('/get_info?ip=8.8.8.8')
    assert response.status_code == 200
