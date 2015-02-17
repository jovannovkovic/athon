from itertools import izip as zip, count, compress

from athon import models, serializers, enums

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


class FallowingUserView(generics.ListAPIView):
    model = models.AthonUser
    serializer_class = serializers.FallowSerializer
    paginate_by = 20

    def get_queryset(self):
        # user_id = self.request.DATA.get('id', None)
        user_id = self.kwargs['id']
        if user_id:
            try:
                athon_user = models.AthonUser.objects.get(id=user_id)
                fallowing_list = athon_user.fallowing.filter(request_status=False)
                request_user = self.request.user.athon_user
                user_fallow_list = list(request_user.fallowing.filter(
                    request_status=False).values_list('followed_user_id', flat=True))
                return chain_fallow_list(fallowing_list, user_fallow_list, request_user.id)
            except models.AthonUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            athon_user = self.request.user.athon_user
        fallowing_list = athon_user.fallowing.filter(request_status=False)
        return map(lambda relationship: {'user': relationship.followed_user,
                                         'fallow_status': 'Fallowing', 'request_status': False}, fallowing_list)


def chain_fallow_list(fallow_list, user_fallow_list, user_id):
    l = map(lambda relationship: {'user': relationship.followed_user, 'fallow_status': 'Fallowing',
            'request_status': False} if relationship.followed_user_id in user_fallow_list else
            {'user': relationship.followed_user, 'fallow_status': 'Fallow', 'request_status': False},
            fallow_list)
    index = [i for i, j in zip(count(), l) if j['user'].id == user_id]
    if index:
        l.insert(0, l.pop(index[0]))
        l[0]['fallow_status'] = '-'
    return l


class FallowersUserView(generics.ListAPIView):
    model = models.AthonUser
    serializer_class = serializers.FallowSerializer
    paginate_by = 20

    def get_queryset(self):
        # user_id = self.request.DATA.get('id', None)
        user_id = self.kwargs['id']
        if int(user_id) > 0:
            try:
                athon_user = models.AthonUser.objects.get(id=user_id)
                fallowers_list = athon_user.fallowers.all()
                request_user = self.request.user.athon_user
                user_fallow_list = list(request_user.fallowing.filter()
                        .values_list('followed_user_id', flat=True))
                return chain_fallowers_list(fallowers_list, user_fallow_list, request_user.id)
            except models.AthonUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            athon_user = self.request.user.athon_user
        fallowers_list = athon_user.fallowers.all()
        return map(lambda relationship: {'user': relationship.follower, 'fallow_status': relationship.fallow_status,
            'request_status': relationship.request_status}, fallowers_list)


def chain_fallowers_list(fallow_list, user_fallow_list, user_id):
    l = map(lambda relationship: {'user': relationship.follower, 'fallow_status': 'Fallowing',
            'request_status': False} if
            relationship.follower_id in user_fallow_list else {'user': relationship.follower,
            'fallow_status': 'Fallow', 'request_status': False}, fallow_list)
    index = [i for i, j in zip(count(), l) if j['user'].id == user_id]
    if index:
        l.insert(0, l.pop(index[0]))
        l[0]['fallow_status'] = '-'
    return l



