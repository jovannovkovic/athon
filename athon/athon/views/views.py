from athon import models, serializers

from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError

from rest_framework import viewsets, mixins, permissions, \
        generics
from rest_framework import status
from rest_framework.response import Response


class IndexView(TemplateView):
    template_name = "index.html"


class _UserManagementViews(viewsets.GenericViewSet):
    """ Parent views class for user's management API calls.
    """
    # Note that permission classes must be set in children classes.
    model = models.AthonUser
    serializer_class = serializers.AthonUserSerializer

    def pre_save(self, obj):
        """ We have to encode the password in the user object that will be
        saved before saving it.
        """
        viewsets.GenericViewSet.pre_save(self, obj)
        if "password" in self.request.DATA.get("user", []):
            # Password is raw right now, so set it properly (encoded password
            # will overwrite the raw one then).
            obj.user.set_password(obj.user.password)


class AthonUserView(mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin, _UserManagementViews):
    """ API enpoint to fetch or update data about a single user.
    The caller has to be logged in as that user or as administrator.

    """

    def pre_save(self, obj):
        """ We have to use both inherited pre_save methods here.
        """
        _UserManagementViews.pre_save(self, obj)
        mixins.UpdateModelMixin.pre_save(self, obj)


class FallowUserView(generics.CreateAPIView):
    model = models.AthonUser

    def post(self, request, *args, **kwargs):
        fallower = self.request.user.athon_user
        fallowed_id = self.request.DATA['id']
        try:
            fallowed = models.AthonUser.objects.get(id=fallowed_id)
        except models.AthonUser.DoesNotExist:
            return Response(data={"Can't fallow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.AthonUser.objects.fallow(fallower, fallowed):
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"Can't fallow. User is private."},
                status=status.HTTP_400_BAD_REQUEST)


class UnFallowUserView(generics.CreateAPIView):
    model = models.AthonUser

    def post(self, request, *args, **kwargs):
        fallower = self.request.user.athon_user
        fallowed_id = self.request.DATA['id']
        try:
            fallowed = models.AthonUser.objects.get(id=fallowed_id)
        except models.AthonUser.DoesNotExist:
            return Response(data={"Can't unfallow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.AthonUser.objects.unfallow(fallower, fallowed):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't unfallow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)


class RequestToFallowUserView(generics.CreateAPIView):
    model = models.AthonUser

    def post(self, request, *args, **kwargs):
        fallower = self.request.user.athon_user
        fallowed_id = self.request.DATA['id']
        try:
            fallowed = models.AthonUser.objects.get(id=fallowed_id)
        except models.AthonUser.DoesNotExist:
            return Response(data={"Can't request to fallow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.AthonUser.objects.request_to_fallow(fallower, fallowed):
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"Can't request to fallow. User is not private."},
                status=status.HTTP_400_BAD_REQUEST)


class RemoveRequestToFallowUserView(generics.CreateAPIView):
    model = models.AthonUser

    def post(self, request, *args, **kwargs):
        fallower = self.request.user.athon_user
        fallowed_id = self.request.DATA['id']
        try:
            fallowed = models.AthonUser.objects.get(id=fallowed_id)
        except models.AthonUser.DoesNotExist:
            return Response(data={"Can't remove request to fallow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.AthonUser.objects.remove_request(fallower, fallowed):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't remove request to fallow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)


class AcceptRequestToFallowUserView(generics.CreateAPIView):
    model = models.AthonUser

    def post(self, request, *args, **kwargs):
        fallowed_user = self.request.user.athon_user
        fallower_id = self.request.DATA['id']
        try:
            fallower = models.AthonUser.objects.get(id=fallower_id)
        except models.AthonUser.DoesNotExist:
            return Response(data={"Can't accept request to fallow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.AthonUser.objects.accept_request(fallower, fallowed_user):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't accept request to fallow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)

