import pytest
import os

from app import app, db

# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Anonymous' in response.data


def test_login(client):
    client.post('/login', data={"user_name": "Test User", "user_email": "test@user.com",
                                "user_password": "password123"})
    response = client.get('/profile')
    assert b"Test User" in response.data

