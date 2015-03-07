from datetime import datetime, date, time
from itertools import izip as zip, count, compress

from athon import models, serializers, enums, permissions

from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import viewsets, mixins, \
        generics, views, permissions as rest_permissions
from rest_framework import status
from rest_framework.response import Response


class IndexView(TemplateView):
    template_name = "index.html"


class _UserManagementViews(viewsets.GenericViewSet):
    """ Parent views class for user's management API calls.
    """
    # Note that permission classes must be set in children classes.
    # model = models.AthonUser
    # serializer_class = serializers.AthonUserSerializer
    model = get_user_model()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsUserOrAdmin,)

    def pre_save(self, obj):
        """ We have to encode the password in the user object that will be
        saved before saving it.
        """
        viewsets.GenericViewSet.pre_save(self, obj)
        if "password" in self.request.DATA:
            # Password is raw right now, so set it properly (encoded password
            # will overwrite the raw one then).
            obj.set_password(obj.password)


class ProfileView(mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin, _UserManagementViews):
    """ API enpoint to fetch or update data about a single user.
    The caller has to be logged in as that user or as administrator.

    """

    def update(self, request, *args, **kwargs):
        if "birthday" in self.request.DATA['profile']:
            b = self.request.DATA['profile']['birthday']
            birthday = date(b[0], b[1], b[2])
            self.request.DATA['profile']['birthday'] = birthday
        return super(ProfileView, self).update(request, *args, **kwargs)

    def pre_save(self, obj):
        """ We have to use both inherited pre_save methods here.
        """
        _UserManagementViews.pre_save(self, obj)
        mixins.UpdateModelMixin.pre_save(self, obj)


class ProfileUserView(generics.UpdateAPIView, generics.GenericAPIView):

    model = models.Profile
    serializer_class = serializers.ProfileSerializer

    def patch(self, request, *args, **kwargs):
        if "birthday" in self.request.DATA['profile']:
            b = self.request.DATA['profile']['birthday']
            birthday = date(b[0], b[1], b[2])
            self.request.DATA['profile']['birthday'] = birthday
        serializer = self.serializer_class(data=self.request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteHistoryView(generics.CreateAPIView):

    model = models.AthleteHistory
    serializer_class = serializers.AthleteHistorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA, many=True,
                        context={'profile': self.request.user.profile})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteHistoryDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    model = models.AthleteHistory
    serializer_class = serializers.AthleteHistorySerializer

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('id', None)
        try:
            athlete_history = models.AthleteHistory.objects.get(pk=pk,
                        profile=self.request.user.profile)
        except models.AthleteHistory.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(athlete_history, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('id', None)
        try:
            athlete_history = models.AthleteHistory.objects.get(pk=pk,
                        profile=self.request.user.profile)
        except models.AthleteHistory.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        athlete_history.delete()
        return Response(status=status.HTTP_200_OK)


class FollowUserView(views.APIView):
    # model = models.FollowUsers

    def post(self, request, *args, **kwargs):
        follower = self.request.user.profile
        followed_id = self.kwargs['id']
        try:
            followed = models.Profile.objects.get(id=followed_id)
        except models.Profile.DoesNotExist:
            return Response(data={"Can't follow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.Profile.objects.follow(follower, followed):
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"Can't follow. User is private."},
                status=status.HTTP_400_BAD_REQUEST)


class UnFollowUserView(views.APIView):

    def post(self, request, *args, **kwargs):
        follower = self.request.user.profile
        followed_id = self.kwargs['id']
        try:
            followed = models.Profile.objects.get(id=followed_id)
        except models.Profile.DoesNotExist:
            return Response(data={"Can't unfollow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.Profile.objects.unfollow(follower, followed):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't unfollow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)


class RequestToFollowUserView(views.APIView):

    def post(self, request, *args, **kwargs):
        follower = self.request.user.profile
        followed_id = self.kwargs['id']
        try:
            followed = models.Profile.objects.get(id=followed_id)
        except models.Profile.DoesNotExist:
            return Response(data={"Can't request to follow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.Profile.objects.request_to_follow(follower, followed):
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"Can't request to follow. User is not private."},
                status=status.HTTP_400_BAD_REQUEST)


class RemoveRequestToFollowUserView(views.APIView):

    def post(self, request, *args, **kwargs):
        follower = self.request.user.profile
        followed_id = self.kwargs['id']
        try:
            followed = models.Profile.objects.get(id=followed_id)
        except models.Profile.DoesNotExist:
            return Response(data={"Can't remove request to follow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.Profile.objects.remove_request(follower, followed):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't remove request to follow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)


class AcceptRequestToFollowUserView(views.APIView):

    def post(self, request, *args, **kwargs):
        followed_user = self.request.user.profile
        follower_id = self.kwargs['id']
        try:
            follower = models.Profile.objects.get(id=follower_id)
        except models.Profile.DoesNotExist:
            return Response(data={"Can't accept request to follow. User does not exist."},
                    status=status.HTTP_404_NOT_FOUND)
        if models.Profile.objects.accept_request(follower, followed_user):
            return Response(status=status.HTTP_200_OK)
        return Response(data={"Can't accept request to follow. Relationship does not exist."},
                status=status.HTTP_400_BAD_REQUEST)


class FollowingUserView(generics.ListAPIView):
    model = models.FollowUsers
    serializer_class = serializers.FollowSerializer
    paginate_by = 20

    def get_queryset(self):
        athon_user = self.request.user.profile
        user_id = self.kwargs['id']
        if athon_user.id != user_id:
            try:
                f_user = models.Profile.objects.get(id=user_id)
                following_list = f_user.following.filter(request_status=False)
                user_follow_list = list(athon_user.following.filter(
                    request_status=False).values_list('followed_user_id', flat=True))
                return chain_follow_list(following_list, user_follow_list, athon_user.id)
            except models.Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        following_list = athon_user.following.filter(request_status=False)
        return map(lambda relationship: {'user': relationship.followed_user,
                                         'follow_status': 'Following', 'request_status': False}, following_list)


def chain_follow_list(follow_list, user_follow_list, user_id):
    l = map(lambda relationship: {'user': relationship.followed_user, 'follow_status': 'Following',
            'request_status': False} if relationship.followed_user_id in user_follow_list else
            {'user': relationship.followed_user, 'follow_status': 'Follow', 'request_status': False},
            follow_list)
    index = [i for i, j in zip(count(), l) if j['user'].id == user_id]
    if index:
        l.insert(0, l.pop(index[0]))
        l[0]['follow_status'] = '-'
    return l


class FollowersUserView(generics.ListAPIView):
    model = models.FollowUsers
    serializer_class = serializers.FollowSerializer
    paginate_by = 20

    def get_queryset(self):
        athon_user = self.request.user.profile
        user_id = self.kwargs['id']
        if athon_user.id != user_id:
            try:
                f_user = models.Profile.objects.get(id=user_id)
                followers_list = f_user.followers.all()
                user_follow_list = list(athon_user.following.filter()
                        .values_list('followed_user_id', flat=True))
                return chain_followers_list(followers_list, user_follow_list, athon_user.id)
            except models.Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        followers_list = athon_user.followers.all()
        return map(lambda relationship: {'user': relationship.follower, 'follow_status': relationship.follow_status,
            'request_status': relationship.request_status}, followers_list)


def chain_followers_list(follow_list, user_follow_list, user_id):
    l = map(lambda relationship: {'user': relationship.follower, 'follow_status': 'Following',
            'request_status': False} if
            relationship.follower_id in user_follow_list else {'user': relationship.follower,
            'follow_status': 'Follow', 'request_status': False}, follow_list)
    index = [i for i, j in zip(count(), l) if j['user'].id == user_id]
    if index:
        l.insert(0, l.pop(index[0]))
        l[0]['follow_status'] = '-'
    return l


class SportView(generics.ListAPIView):
    model = models.Sport

    def get_queryset(self):
        return models.Sport.objects.all()


class UnitView(generics.ListAPIView):
    model = models.Unit

    def get_queryset(self):
        return models.Unit.objects.all()


class ActivityTypeView(generics.ListAPIView):
    model = models.ActivityType

    def get_queryset(self):
        return models.ActivityType.objects.all()


class ExerciseTypeView(generics.ListAPIView):
    model = models.ExerciseType
    serializer_class = serializers.ExerciseTypeSerializer

    def get_queryset(self):
        return models.ExerciseType.objects.all()


class PostView(generics.ListCreateAPIView):
    model = models.Post
    serializer_class = serializers.PostSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        data = request.DATA
        if 'duration' in data:
            d = data['duration']
            duration = time(d[0], d[1], d[2])
            data['duration'] = duration
        serializer = self.serializer_class(data=data,
                        context={'user': self.request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        following_ids = self.request.user.profile.following.filter(
                request_status=False).values_list('followed_user__user_id', flat=True)
        return models.Post.objects.filter(user_id__in=following_ids)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = models.Post
    serializer_class = serializers.PostSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        models.Post.objects.filter(id=id).update(hidden=True)
        return Response(status=status.HTTP_200_OK)

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('id', None)
        try:
            return self.model.objects.get(id=post_id)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pass


class UserPostView(generics.ListAPIView):
    model = models.Post
    serializer_class = serializers.PostSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)
    paginate_by = 20

    def get_queryset(self):
        user_id = self.kwargs.get('id', None)
        return models.Post.objects.filter(user_id=user_id)
