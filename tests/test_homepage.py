from page_analyzer import app


def test_homepage():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b"<title> Homepage </title>" in response.data
    assert b"Hello from Greg!" in response.data
