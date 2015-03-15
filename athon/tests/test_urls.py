from os import path
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
    assert user.is_active == True
    assert user.profile is not None
    assert models.RegistrationProfile.objects.get(user=user).activation_key != models.RegistrationProfile.ACTIVATED


@pytest.mark.django_db
def test_user_login_before_activation():
    """ Testing the login before activation proces. """

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
    assert user.is_active == True
    assert user.profile is not None
    assert models.RegistrationProfile.objects.get(user=user).activation_key != models.RegistrationProfile.ACTIVATED

    response = api_client.post(
        "/api/user/login/",
        {
            "username": USERNAME, "password": PASSWORD
        },
        format='json')

    print response
    assert response.status_code == status.HTTP_200_OK


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

    assert response.status_code == status.HTTP_200_OK
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
    a_user = get_user_model().objects.get(username=TEST_USERNAME)

    response = logged_client.get(
        "/api/user/%s/.json" % a_user.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk

    response = logged_client.get(
        "/api/user/%s/.json" % another_user.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == another_user.pk


@pytest.mark.django_db
def test_update_user(logged_client, another_user):
    """ Test updating user. """
    a_user = get_user_model().objects.get(username=TEST_USERNAME)
    hometown = 'Beograd'
    response = logged_client.patch(
        "/api/user/%s/.json" % a_user.pk,
        {
            'profile': {
                'hometown': hometown,
                'birthday': [2011, 2, 1]
            }
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['profile']['hometown'] == hometown
    first_name = 'another_user'
    height = 123
    response = logged_client.patch(
        "/api/user/%s/" % a_user.pk,
        {
            'first_name': first_name,
            'profile': {
                'hometown': hometown,
                'height': height
            }
        }, format='json')
    a_user = get_user_model().objects.get(username=TEST_USERNAME)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk
    assert response.data['first_name'] == first_name
    assert response.data['profile']['height'] == height

    response = logged_client.patch(
        "/api/user/%s/" % a_user.pk,
        {
            'password': 'joca',
            'profile': {
                'hometown': hometown
            }
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk
    assert get_user_model().objects.get(username=TEST_USERNAME).check_password('joca') is True

    first_name = 'another_user'
    height = 123
    response = logged_client.patch(
        "/api/user/%s/" % a_user.pk,
        {
            'first_name': first_name,
            'profile': {
                'hometown': hometown,
                'height': height,

            }
        }, format='json')
    print response
    a_user = get_user_model().objects.get(username=TEST_USERNAME)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == a_user.pk
    assert response.data['first_name'] == first_name
    assert response.data['profile']['height'] == height


@pytest.mark.django_db
def test_user_create_athlete_histories(logged_client, sports):
    response = logged_client.post(
        "/api/user/athlete_history/",
            [
                {
                    'sport': sports[0].id,
                    'from_date': 2003,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player1'
                        },
                        {
                            'title': 'TOP Goalscorer'
                        }
                    ]
                },
                {
                    'sport': sports[1].id,
                    'from_date': 2005,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player'
                        }
                    ]
                }
            ]
        , format='json')
    print response
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 2

    response = logged_client.post(
        "/api/user/athlete_history/",
            [
                {
                    'sport': sports[1].id,
                    'from_date': 2005,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player'
                        }
                    ]
                }
            ]
        , format='json')
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert response.status_code == status.HTTP_201_CREATED
    assert a_user.athlete_histories.count() == 3


@pytest.mark.django_db
def test_user_update_athlete_histories(logged_client, sports):
    logged_client.post(
        "/api/user/athlete_history/",
            [
                {
                    'sport': sports[1].id,
                    'from_date': 2003,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player1'
                        }
                    ]
                },
                {
                    'sport': sports[0].id,
                    'from_date': 2005,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player'
                        }
                    ]
                }
            ]
        , format='json')
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    ah = a_user.athlete_histories.all()[0]
    response = logged_client.put(
        "/api/user/athlete_history/%s/" % ah.id,
            {
                'sport': sports[1].id,
            }
        , format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['sport'] == sports[1].id
    assert response.data['id'] == ah.id

    ach = ah.achievements.all()[0]
    title = 'TOP'
    response = logged_client.put(
        "/api/user/athlete_history/%s/" % ah.id,
            {
                'sport': sports[0].id,
                'from_date': 2005,
                'until_date': 2004,
                'achievements': [
                    {
                        'id': ach.pk,
                        'title': title
                    }
                ]
            }
        , format='json')
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert response.status_code == status.HTTP_200_OK
    assert response.data['achievements'][0]['title'] == title
    assert a_user.athlete_histories.count() == 2


@pytest.mark.django_db
def test_user_delete_athlete_histories(logged_client, sports):
    response = logged_client.post(
        "/api/user/athlete_history/",
            [
                {
                    'sport': sports[0].id,
                    'from_date': 2003,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player1'
                        }
                    ]
                },
                {
                    'sport': sports[1].id,
                    'from_date': 2005,
                    'until_date': 2005,
                    'achievements': [
                        {
                            'title': 'Best player'
                        }
                    ]
                }
            ]
        , format='json')
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    ah_set = a_user.athlete_histories.all()
    assert ah_set.count() == 2
    ah_first_id = response.data[0]['id']
    response = logged_client.delete(
        "/api/user/athlete_history/%s/" % response.data[1]['id'])
    assert response.status_code == status.HTTP_200_OK
    ah_set = a_user.athlete_histories.all()
    assert ah_set[0].id == ah_first_id
    assert ah_set.count() == 1


@pytest.mark.django_db
def test_user_update_image(logged_client):
    """ Test if we can store some image as user profile image.
    """
    a_user = get_user_model().objects.get(username=TEST_USERNAME)
    user_id = a_user.pk
    with open(path.join(path.dirname(__file__), "pixel.jpg")) as file_ptr:
        response = logged_client.put(
            "/api/user/profile/%s/" % user_id,
            {
                'profile_photo': file_ptr,
                'hometown': 'Ub'
            }
        )
    print response
    assert response.status_code == status.HTTP_200_OK

    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    print a_user.profile_photo.url
    assert a_user.profile_photo.url.startswith(
            "https://athon.s3.amazonaws.com/media/athon/profile/")
    assert a_user.hometown == 'Ub'


@pytest.mark.django_db
def test_search_user(logged_client, another_user, user_mika):
    search_term = 'TESTING'
    response = logged_client.get(
        "/api/user/search_for_user/", {'search_term': search_term})
    print response
    assert response.data['count'] == 2
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_follow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    response = logged_client.post(
        "/api/user/%s/follow/" % another_user.pk)

    assert a_user.following.filter(followed_user=another_user).count() == 1
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_follow_private_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    another_user.profile.is_public_profile = False
    another_user.profile.save()
    response = logged_client.post(
        "/api/user/%s/follow/" % another_user.pk)
    assert a_user.following.filter(followed_user=another_user).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_follow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/%s/follow/" % user_id)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unfollow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    an_user = another_user.profile
    models.FollowUsers.objects.create(follower=a_user, followed_user=an_user)
    a_user.following_number = 1
    a_user.save()
    an_user.followers_number = 1
    an_user.save()
    assert a_user.following.filter(followed_user=another_user.profile).count() == 1
    response = logged_client.post(
        "/api/user/%s/unfollow/" % another_user.pk)

    assert a_user.following.filter(followed_user=another_user.profile).count() == 0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_request_to_follow_user(logged_client, another_user):
    another_user.profile.is_public_profile = False
    another_user.profile.save()
    response = logged_client.post(
        "/api/user/%s/request_to_follow/" % another_user.pk)

    assert another_user.profile.followers.filter(request_status=True).count() == 1
    assert response.status_code == status.HTTP_201_CREATED
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert a_user.following_number == 0


@pytest.mark.django_db
def test_request_to_follow_public_user(logged_client, another_user):
    another_user.profile.is_public_profile = True
    another_user.profile.save()
    response = logged_client.post(
        "/api/user/%s/request_to_follow/" % another_user.pk)
    assert another_user.profile.followers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert a_user.following_number == 0


@pytest.mark.django_db
def test_request_to_follow_non_existing_user(logged_client, another_user):
    another_user.profile.is_public_profile = False
    another_user.profile.save()
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/%s/request_to_follow/" % user_id)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_request_to_follow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    models.FollowUsers.objects.create(follower=a_user,
            followed_user=another_user.profile, request_status=True)
    assert another_user.profile.followers.filter(request_status=True).count() == 1
    response = logged_client.post(
        "/api/user/%s/remove_request_to_follow/" % another_user.pk)

    assert another_user.profile.followers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_200_OK
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert a_user.following_number == 0


@pytest.mark.django_db
def test_remove_request_to_follow_not_existing_relationship(logged_client, another_user):
    another_user.profile.is_public_profile = True
    another_user.profile.save()
    response = logged_client.post(
        "/api/user/%s/remove_request_to_follow/" % another_user.pk)
    assert another_user.profile.followers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_remove_request_to_follow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/%s/remove_request_to_follow/" % user_id)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_accept_request_to_follow_user(logged_client, another_user):
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    models.FollowUsers.objects.create(follower=another_user.profile,
            followed_user=a_user, request_status=True)
    assert a_user.followers.filter(request_status=True).count() == 1
    response = logged_client.post(
        "/api/user/%s/accept_request/" % another_user.pk)

    assert a_user.followers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_200_OK
    a_user = get_user_model().objects.get(username=TEST_USERNAME).profile
    assert a_user.followers_number == 1
    another_user = get_user_model().objects.get(id=another_user.pk).profile
    assert another_user.following_number == 1


@pytest.mark.django_db
def test_accept_request_to_follow_not_existing_relationship(logged_client, another_user):
    response = logged_client.post(
        "/api/user/%s/accept_request/" % another_user.pk)
    assert another_user.profile.followers.filter(request_status=True).count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_accept_request_to_follow_non_existing_user(logged_client, another_user):
    user_id = another_user.pk + 1
    response = logged_client.post(
        "/api/user/%s/accept_request/" % user_id)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_username_exist(api_client, user):
    response = api_client.post(
        "/api/user/available/username/",
        {
            'username': TEST_USERNAME_1,
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    response = api_client.post(
        "/api/user/available/username/",
        {
            'username': TEST_USERNAME,
        }, format='json')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_email_exist(api_client, user):
    response = api_client.post(
        "/api/user/available/email/",
        {
            'email': TEST_EMAIL_1,
        }, format='json')
    assert response.status_code == status.HTTP_200_OK
    response = api_client.post(
        "/api/user/available/email/",
        {
            'email': TEST_EMAIL,
        }, format='json')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_user_post(logged_client, another_user, exercise_type):
    units = models.Unit.objects.all()
    user =  get_user_model().objects.get(username=TEST_USERNAME)
    logged_client = APIClient()
    logged_client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
    logged_client.force_authenticate(user=user)
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'activity_details': {
                'rounds': '3-5-5',
                'interval': '7 minuta',
                'amrap': [1, 2]
            },
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 45,
                    'repetition': 10
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 55,
                    'repetition': 8
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    print response
    assert response.status_code == status.HTTP_201_CREATED
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_get(logged_client, another_user, user_mika, exercise_type):
    units = models.Unit.objects.all()
    response = logged_client.post(
        "/api/user/%s/follow/" % another_user.pk)
    another_user_client = APIClient()
    another_user_client.login(username=TEST_USERNAME_1, password=TEST_PASSWORD_1)
    another_user_client.force_authenticate(user=another_user)

    user_mika_client = APIClient()
    user_mika_client.login(username=TEST_USERNAME_2, password=TEST_PASSWORD_2)
    user_mika_client.force_authenticate(user=user_mika)

    response = another_user_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 45,
                    'repetition': 10
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 55,
                    'repetition': 8
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    response = user_mika_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    response = logged_client.get(
        "/api/post/")
    assert len(response.data['results']) == 1
    assert response.data['count'] == 1
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_get_not_fallowing(logged_client):
    response = logged_client.get(
        "/api/post/")
    print response
    assert len(response.data['results']) == 0
    assert response.data['count'] == 0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_delete(logged_client, another_user, user_mika, exercise_type):
    units = models.Unit.objects.all()
    response = logged_client.post(
        "/api/user/%s/follow/" % another_user.pk)
    another_user_client = APIClient()
    another_user_client.login(username=TEST_USERNAME_1, password=TEST_PASSWORD_1)
    another_user_client.force_authenticate(user=another_user)

    user_mika_client = APIClient()
    user_mika_client.login(username=TEST_USERNAME_2, password=TEST_PASSWORD_2)
    user_mika_client.force_authenticate(user=user_mika)

    response = another_user_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 45,
                    'repetition': 10
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 55,
                    'repetition': 8
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    post_id = response.data['id']
    response = user_mika_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    response = logged_client.get(
        "/api/post/")
    assert len(response.data['results']) == 1
    assert response.data['count'] == 1
    assert response.status_code == status.HTTP_200_OK

    response = another_user_client.delete(
        "/api/post/%s/" % post_id
    )
    assert response.status_code == status.HTTP_200_OK

    response = logged_client.get(
        "/api/post/")
    assert len(response.data['results']) == 0
    assert response.data['count'] == 0
    assert response.status_code == status.HTTP_200_OK

    assert models.Post.objects.count() == 1

@pytest.mark.django_db
def test_user_post_like(logged_client, another_user, exercise_type):
    units = models.Unit.objects.all()
    user = get_user_model().objects.get(username=TEST_USERNAME)
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'activity_details': {
                'rounds': '3-5-5',
                'interval': '7 minuta',
                'amrap': [1, 2]
            },
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 45,
                    'repetition': 10
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 55,
                    'repetition': 8
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    print response
    post_id = response.data['id']
    assert response.status_code == status.HTTP_201_CREATED
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    response = logged_client.post(
        "/api/post/%s/like/" % post_id)
    post = models.Post.objects.get(id=post_id)
    assert post.like_number == 1
    assert response.status_code == status.HTTP_200_OK

    response = logged_client.get(
        "/api/post/%s/like/" % post_id)
    assert response.status_code == status.HTTP_200_OK

    response = logged_client.delete(
        "/api/post/%s/like/" % post_id)
    post = models.Post.objects.get(id=post_id)
    assert post.like_number == 0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_post_comment(logged_client, another_user, exercise_type):
    units = models.Unit.objects.all()
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'activity_details': {
                'rounds': '3-5-5',
                'interval': '7 minuta',
                'amrap': [1, 2]
            },
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 45,
                    'repetition': 10
                    },
                    {
                    'unit': units[0].id,
                    'quantity': 55,
                    'repetition': 8
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    },
                    {
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    post_id = response.data['id']
    assert response.status_code == status.HTTP_201_CREATED
    response = logged_client.post(
        "/api/post/", {
            'title': 'Gym',
            'activity_name': 'Biceps i triceps',
            'status': 'Vrhunski',
            'location': 'Fit&Health Vracar',
            'time': 2153,
            'exercise': [{
                'type': exercise_type[0].id,
                'reps':[{
                    'unit': units[0].id,
                    'quantity': 35,
                    'repetition': 12
                    }]
                },
                {
                'type': exercise_type[1].id,
                'reps':[{
                    'repetition': 20
                    }]
                }
            ]

        }, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    comment = 'Kakav fenomenalan trenig. Isplati se raditi po tvom programu.' \
              'Nadam se da ces me prihvatiti za prijatelja. Pozzz'
    response = logged_client.post(
        "/api/post/%s/comment/" % post_id,
        {
            'comment': comment
        }, format='json')
    post = models.Post.objects.get(id=post_id)
    assert post.comment_number == 1
    assert response.status_code == status.HTTP_200_OK

    response = logged_client.get(
        "/api/post/%s/comment/" % post_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['comment'] == comment

    response = logged_client.delete(
        "/api/post/%s/comment/" % post_id)
    post = models.Post.objects.get(id=post_id)
    assert post.comment_number == 0
    assert response.status_code == status.HTTP_200_OK