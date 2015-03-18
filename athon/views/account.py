import datetime

from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.sites.models import RequestSite, Site
from django.utils import timezone
from django.utils.http import base36_to_int
from django.utils.translation import gettext_lazy as _

from rest_framework import status, generics, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from athon.models import RegistrationProfile, PasswordReset
from athon.signals import user_registered
from athon.permissions import IsNotAuthenticated
from athon.serializers import UserSerializer, ResetPasswordKeySerializer,\
        ResetPasswordSerializer


REGISTRATION_ALLOWED_FOR = 10


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
    model = get_user_model()

    def post(self, request):
        activation_key = request.QUERY_PARAMS.get('ac')
        user = RegistrationProfile.objects.activate_user(activation_key)
        login(request, user)
        return Response(UserSerializer(user).data)


class AuthenticateView(APIView):
    permission_classes = [AllowAny]
    model = get_user_model()

    def post(self, request):
        username = data(request, 'username')
        password = data(request, 'password')
        user = authenticate(username=username, password=password)
        if user is not None:
            profile = user.profile
            if profile.is_active:
                login(request, user)
                return Response(UserSerializer(user).data)
            else:
                if self.is_allowed_to_login(user):
                    login(request, user)
                    return Response(UserSerializer(user).data)
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def is_allowed_to_login(self, user):
        if (user.date_joined + datetime.timedelta(minutes=REGISTRATION_ALLOWED_FOR)) < timezone.now():
            return False
        return True


class CheckUsernameView(APIView):
    """ Check if user with sent username exist. If exist return status 200,
    else API call will break.

    """

    permission_classes = [AllowAny]
    model = get_user_model()

    def post(self, request):
        username = data(request, 'username')
        try:
            user = get_user_model().objects.get(username=username)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_200_OK)


class CheckEmailView(APIView):
    """ Check if user with sent email exist. If exist, return status 200,
    else API call will break.

    """

    permission_classes = [AllowAny]
    model = get_user_model()

    def post(self, request):
        email = data(request, 'email')
        try:
            user = get_user_model().objects.get(email=email)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_200_OK)


class CheckSessionView(APIView):
    permission_classes = [AllowAny]
    model = get_user_model()

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PasswordResetRequestKey(generics.GenericAPIView):
    """
    Sends an email to the user email address with a link to reset his password.

    **TODO:** the key should be sent via push notification too.

    **Accepted parameters:**

     * email
    """
    permission_classes = (IsNotAuthenticated, )
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        # init form with POST data
        serializer = self.serializer_class(data=request.DATA)
        # validate
        if serializer.is_valid():
            serializer.save()
            return Response({
                'detail': _(u'We just sent you the link with which you'
                        u' will able to reset your password at %s') % request.DATA.get('email')
            })
        # in case of errors
        return Response(serializer.errors, status=400)

    def permission_denied(self, request):
        raise exceptions.PermissionDenied(_("You can't reset your password"
                        " if you are already authenticated"))

account_password_reset = PasswordResetRequestKey.as_view()


class PasswordResetFromKey(generics.GenericAPIView):
    """
    Reset password from key.

    **The key must be part of the URL**!

    **Accepted parameters:**

     * password1
     * password2
    """

    permission_classes = (IsNotAuthenticated, )
    serializer_class = ResetPasswordKeySerializer

    def post(self, request, uidb36, key, format=None):
        # pull out user
        try:
            uid_int = base36_to_int(uidb36)
            password_reset_key = PasswordReset.objects.get(user_id=uid_int, temp_key=key, reset=False)
        except (ValueError, PasswordReset.DoesNotExist, AttributeError):
            return Response({'errors': _(u'Key Not Found')}, status=404)

        serializer = ResetPasswordKeySerializer(
            data=request.DATA,
            instance=password_reset_key
        )

        # validate
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': _(u'Password successfully changed.')})
        # in case of errors
        return Response(serializer.errors, status=400)

    def permission_denied(self, request):
        raise exceptions.PermissionDenied(_("You can't reset your password if you are already authenticated"))

account_password_reset_key = PasswordResetFromKey.as_view()
