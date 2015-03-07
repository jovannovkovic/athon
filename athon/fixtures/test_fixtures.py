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

TEST_EMAIL_2 = 'neki2@test.com'
TEST_USERNAME_2 = "MIKA"
TEST_PASSWORD_2 = "paswordija 111"

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
def user_mika():
    user = User(username=TEST_USERNAME_2, email=TEST_EMAIL_2)
    user.set_password(TEST_PASSWORD_2)
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


@pytest.fixture
def sports():
    sport1 = models.Sport.objects.create(name='Fudbal')
    sport2 = models.Sport.objects.create(name='Kosarka')
    return [sport1, sport2]


@pytest.fixture
def units():
    unit1 = models.Unit.objects.create(name='Kilogram', hint='kg')
    unit2 = models.Unit.objects.create(name='Metar', hint='m')
    unit3 = models.Unit.objects.create(name='Kilometar', hint='km')
    return [unit1, unit2, unit3]


@pytest.fixture
def exercise_type(units):
    ex1 = models.ExerciseType.objects.create(name='Bench Press', unit=units[0], quantity=True, repetition=True)
    ex2 = models.ExerciseType.objects.create(name='Push ups', quantity=True, repetition=True)
    ex3 = models.ExerciseType.objects.create(name='Cycling', unit=units[2], quantity=True)
    return [ex1, ex2, ex3]


@pytest.fixture
def activity_type():
    at1 = models.ActivityType.objects.create(name='Rounds', hint='Create training with rounds')
    at2 = models.ActivityType.objects.create(name='Interval training', hint='Create interval training')
    return [at1, at2]
