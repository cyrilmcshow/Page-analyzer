from page_analyzer.app import create_app
import pytest

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_example(client):
    response = client.get("/urls")
    print(response.get_data())

