from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.sites.models import RequestSite, Site

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from athon.models import RegistrationProfile, AthonUser
from athon.serializers import AthonUserSerializer
from athon.signals import user_registered


# helper for extracting data from REST DATA object
def data(request, key):
    return request.DATA.get(key)


class RegistrationView(APIView):
    """ API endpoint for creating (registering) new user.

    """
    permission_classes = [AllowAny]

    def post(self, request):
        username, email, password = \
            data(request, 'username'), \
            data(request, 'email'), \
            data(request, 'password')

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)

        user_registered.send(RegistrationView, user=new_user, request=request)
        return Response(status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    """ API endpoint for activating user.

    """
    permission_classes = [AllowAny]
    model = AthonUser

    def post(self, request):
        activation_key = request.QUERY_PARAMS.get('ac')
        user = RegistrationProfile.objects.activate_user(activation_key)
        login(request, user)
        return Response(AthonUserSerializer(user.athon_user).data)


class AuthenticateView(APIView):
    permission_classes = [AllowAny]
    model = AthonUser

    def post(self, request):
        username = data(request, 'username')
        password = data(request, 'password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(AthonUserSerializer(user.athon_user).data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
