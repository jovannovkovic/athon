import pytest

from athon import models

from django.contrib.auth.models import User
from rest_framework.test import APIClient

TEST_EMAIL = 'neki@test.com'
TEST_USERNAME = "TESTING ERIC"
TEST_PASSWORD = "paswordija"

TEST_EMAIL_1 = 'neki1@test.com'
TEST_USERNAME_1 = "TESTING ERIC VELIKI"
TEST_PASSWORD_1 = "paswordija 111"

@pytest.fixture
def user():
    user = User(username=TEST_USERNAME, email=TEST_EMAIL, is_active=False)
    user.set_password(TEST_PASSWORD)
    user.save()
    models.Profile.create_empty(user)
    return user


@pytest.fixture
def another_user():
    user = User(username=TEST_USERNAME_1, email=TEST_EMAIL_1)
    user.set_password(TEST_PASSWORD_1)
    user.save()
    models.Profile.create_empty(user)
    return user


@pytest.fixture
def logged_client(api_client, user):
    api_client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def api_client():
    return APIClient()



