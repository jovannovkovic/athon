import pytest
import json

from athon import models
from athon.fixtures.test_fixtures import *

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


USERNAME = "jovan"
PASSWORD = "jovan"
EMAIL = "jovan_novko@yahoo.com"


@pytest.mark.django_db
def test_user_registration():
    """ Testing the registration proces. """

    api_client = APIClient()  # not logged in clients should be able to register
    response = api_client.post(
        "/api/user/register/",
        {
            "username": USERNAME, "password": PASSWORD,
            "email": EMAIL,
        },
        format='json')
    assert response.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(username=USERNAME, email=EMAIL)
    assert user is not None
    assert user.is_active == False
    assert user.athon_user is not None
    assert models.RegistrationProfile.objects.get(user=user).activation_key != models.RegistrationProfile.ACTIVATED


@pytest.mark.django_db
def test_user_activate():
    """ Testing activation proces. """

    api_client = APIClient()  # not logged in clients should be able to activate
    response = api_client.post(
        "/api/user/register/",
        {
            "username": USERNAME, "password": PASSWORD,
            "email": EMAIL,
        },
        format='json')
    user = get_user_model().objects.get(username=USERNAME, email=EMAIL)
    profile = models.RegistrationProfile.objects.get(user=user)

    response = api_client.post((
        "/api/user/activate?ac=%s" % profile.activation_key), {})
    print response
    assert response.status_code == status.HTTP_200_OK
    assert models.RegistrationProfile.objects.get(user=user).activation_key == models.RegistrationProfile.ACTIVATED
    user = get_user_model().objects.get(username=USERNAME, email=EMAIL)
    assert user.is_active is True


@pytest.mark.django_db
def test_user_login(api_client, user):
    """ Testing login proces. """

    response = api_client.post(
        "/api/user/login/",
        {
            "username": USERNAME, "password": PASSWORD
        },
        format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = api_client.post(
        "/api/user/login/",
        {
            "username": TEST_USERNAME, "password": TEST_PASSWORD
        },
        format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    user.is_active = True
    user.save()

    response = api_client.post(
        "/api/user/login/",
        {
            "username": TEST_USERNAME, "password": TEST_PASSWORD
        },
        format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_user(logged_client, another_user):
    """ Test returning user. """
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user

    response = logged_client.get(
        "/api/user/by_id/%s/.json" % a_user.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk

    response = logged_client.get(
        "/api/user/by_id/%s/.json" % another_user.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == another_user.pk


@pytest.mark.django_db
def test_update_user(logged_client, another_user):
    """ Test updating user. """
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    hometown = 'Beograd'
    response = logged_client.patch(
        "/api/user/by_id/%s/.json" % a_user.pk,
        {
            'hometown': hometown
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['hometown'] == hometown
    first_name = 'another_user'
    response = logged_client.patch(
        "/api/user/by_id/%s/" % a_user.pk,
        {
            'hometown': hometown,
            'user': {
                    'first_name': first_name
                    }
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk
    assert response.data['user']['first_name'] == first_name

    response = logged_client.patch(
        "/api/user/by_id/%s/" % a_user.pk,
        {
            'hometown': hometown,
            'user': {
                    'password': 'joca'
                    }
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk
    assert get_user_model().objects.get(username=TEST_USERNAME).check_password('joca') is True


@pytest.mark.django_db
def test_fallow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    response = logged_client.post(
        "/api/user/fallow/",
        {
            'followed_user': another_user.pk
        }, format='json')

    assert a_user.fallowing.filter(followed_user=another_user).count() == 1
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_fallow_private_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    another_user.athon_user.is_public_profile = False
    another_user.athon_user.save()
    response = logged_client.post(
        "/api/user/fallow/",
        {
            'followed_user': another_user.pk
        }, format='json')
    assert a_user.fallowing.filter(followed_user=another_user).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_fallow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/fallow/",
        {
            'followed_user': user_id
        }, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unfallow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    an_user = another_user.athon_user
    models.FallowUsers.objects.create(follower=a_user, followed_user=an_user)
    a_user.fallowing_number = 1
    a_user.save()
    an_user.fallowers_number = 1
    an_user.save()
    assert a_user.fallowing.filter(followed_user=another_user.athon_user).count() == 1
    response = logged_client.post(
        "/api/user/unfallow/",
        {
            'id': another_user.pk
        }, format='json')

    assert a_user.fallowing.filter(followed_user=another_user.athon_user).count() == 0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_request_to_fallow_user(logged_client, another_user):
    another_user.athon_user.is_public_profile = False
    another_user.athon_user.save()
    response = logged_client.post(
        "/api/user/request_to_fallow/",
        {
            'id': another_user.pk
        }, format='json')

    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 1
    assert response.status_code == status.HTTP_201_CREATED
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    assert a_user.fallowing_number == 0


@pytest.mark.django_db
def test_request_to_fallow_public_user(logged_client, another_user):
    another_user.athon_user.is_public_profile = True
    another_user.athon_user.save()
    response = logged_client.post(
        "/api/user/request_to_fallow/",
        {
            'id': another_user.pk
        }, format='json')
    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    assert a_user.fallowing_number == 0


@pytest.mark.django_db
def test_request_to_fallow_non_existing_user(logged_client, another_user):
    another_user.athon_user.is_public_profile = False
    another_user.athon_user.save()
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/request_to_fallow/",
        {
            'id': user_id
        }, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_request_to_fallow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    models.FallowUsers.objects.create(follower=a_user,
            followed_user=another_user.athon_user, request_status=True)
    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 1
    response = logged_client.post(
        "/api/user/remove_request_to_fallow/",
        {
            'id': another_user.pk
        }, format='json')

    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_200_OK
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    assert a_user.fallowing_number == 0


@pytest.mark.django_db
def test_remove_request_to_fallow_not_existing_relationship(logged_client, another_user):
    another_user.athon_user.is_public_profile = True
    another_user.athon_user.save()
    response = logged_client.post(
        "/api/user/remove_request_to_fallow/",
        {
            'id': another_user.pk
        }, format='json')
    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_remove_request_to_fallow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/remove_request_to_fallow/",
        {
            'id': user_id
        }, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_accept_request_to_fallow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    models.FallowUsers.objects.create(follower=another_user.athon_user,
            followed_user=a_user, request_status=True)
    assert a_user.fallowers.filter(request_status=True).count() == 1
    response = logged_client.post(
        "/api/user/accept_request/",
        {
            'id': another_user.pk
        }, format='json')

    assert a_user.fallowers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_200_OK
    a_user = get_user_model().objects.get(username=TEST_USERNAME).athon_user
    assert a_user.fallowers_number == 1
    another_user = get_user_model().objects.get(id=another_user.pk).athon_user
    assert another_user.fallowing_number == 1


@pytest.mark.django_db
def test_accept_request_to_fallow_not_existing_relationship(logged_client, another_user):
    response = logged_client.post(
        "/api/user/accept_request/",
        {
            'id': another_user.pk
        }, format='json')
    assert another_user.athon_user.fallowers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_accept_request_to_fallow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/accept_request/",
        {
            'id': user_id
        }, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND




