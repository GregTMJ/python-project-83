import pytest


from page_analyzer import app


@pytest.fixture()
def get_app():
    created_app = app
    created_app.config.update({
        'TESTING': True,
    })

    yield created_app


@pytest.fixture()
def client(get_app):
    return get_app.test_client()


@pytest.fixture()
def runner(get_app):
    return get_app.test_cli_runner()
