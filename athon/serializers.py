import models

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from drf_toolbox.serializers import ModelSerializer as DRFModelSerializer
from rest_framework import serializers

from rest_framework.fields import IntegerField, BooleanField, CharField

PASSWORD_MAX_LENGTH = 50


class _UserSerializer(serializers.ModelSerializer):
    """ For some reason, we cannot use UserSerializer class directly bellow.
    This is the reason why we have this private class here (which has very
    similar Meta class as the parent class).

    """

    class Meta:
        model = get_user_model()
        write_only_fields = ('password',)
        read_only_fields = (
            "groups", "user_permissions", "is_staff", "is_active",
            "is_superuser", "id", "last_login", "date_joined"
        )
        exclude = ('permission', )

    def from_native(self, data, files=None):
        """
        Deserialize primitives -> objects.
        """
        self._errors = {}
        if data is not None or files is not None:
            attrs = self.restore_fields(data, files)
            if attrs is not None:
                attrs = self.perform_validation(attrs)
        else:
            self._errors['non_field_errors'] = ['No input provided']

        if not self._errors:
            return self.restore_object(attrs, instance=getattr(self, 'object', None))


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Achievement
        fields = ('id', 'title', 'year')


class AthleteHistorySerializer(serializers.ModelSerializer):

    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = models.AthleteHistory
        fields = ('id', 'sport', 'from_date', 'until_date', 'achievements', 'profile')

    def save_object(self, obj, **kwargs):
        profile = self.context.get('profile', None)
        if profile is not None:
            obj.profile = profile
        super(AthleteHistorySerializer, self).save_object(obj, **kwargs)


class Photo(serializers.ImageField):

    def to_native(self, value):
        try:
            return value.url
        except ValueError:
            pass
        return super(Photo, self).to_native(value)


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Profile entity which includes django's user entity.

    """
    athlete_histories = AthleteHistorySerializer(many=True, required=False)
    gender = IntegerField(required=False)
    profile_photo = Photo(required=False)

    class Meta:
        model = models.Profile
        read_only_fields = (
            "followers_number", "following_number"
        )
        exclude = ('follow_users', 'user', 'is_active')

    # def to_native(self, obj):
    #     print "b"*60
    #     print obj.profile_photo
    #     if obj.profile_photo is not None or obj.profile_photo is not "":
    #         print "a"*60
    #         obj.profile_photo = obj.profile_photo.url
    #     return super(ProfileSerializer, self).to_native(obj)


class UserSerializer(serializers.ModelSerializer):
    """ For some reason, we cannot use UserSerializer class directly bellow.
    This is the reason why we have this private class here (which has very
    similar Meta class as the parent class).

    """
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        write_only_fields = ('password',)
        read_only_fields = (
             "is_staff", "is_active",
            "is_superuser", "id", "last_login", "date_joined"
        )
        exclude = ('permission', "groups", "user_permissions" )

    def from_native(self, data, files=None):
        """
        Deserialize primitives -> objects.
        """
        self._errors = {}
        if data is not None or files is not None:
            attrs = self.restore_fields(data, files)
            if attrs is not None:
                attrs = self.perform_validation(attrs)
        else:
            self._errors['non_field_errors'] = ['No input provided']

        if not self._errors:
            return self.restore_object(attrs, instance=getattr(self, 'object', None))


class FollowAthonUserSerializer(serializers.ModelSerializer):

    username = serializers.Field(source='user.username')
    first_name = serializers.Field(source='user.first_name')
    last_name = serializers.Field(source='user.last_name')

    class Meta:
        model = models.Profile
        fields = ('id', 'profile_photo', 'username', 'first_name', 'last_name', 'is_public_profile')
        exclude = ('follow_users',)


class FollowSerializer(DRFModelSerializer):

    user = FollowAthonUserSerializer()
    request_status = BooleanField(default=False)
    follow_status = CharField()

    class Meta:
        model = models.FollowUsers
        fields = ('user', 'follow_status', 'request_status')


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self, attrs, source):
        """ ensure email is in the database """

        if not get_user_model().objects.filter(email__iexact=attrs["email"],
                    is_active=True).exists():
            raise serializers.ValidationError(_("Email address not verified for any user account"))

        return attrs

    def restore_object(self, attrs, instance=None):
        """ create password reset for user """
        password_reset = models.PasswordReset.objects.create_for_user(attrs["email"])
        return password_reset


class ResetPasswordKeySerializer(serializers.Serializer):

    password1 = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH
    )
    password2 = serializers.CharField(
        help_text=_('New Password (confirmation)'),
        max_length=PASSWORD_MAX_LENGTH
    )

    def validate_password2(self, attrs, source):
        """
        password2 check
        """
        password_confirmation = attrs[source]
        password = attrs['password1']

        if password_confirmation != password:
            raise serializers.ValidationError(_('Password confirmation mismatch'))

        return attrs

    def restore_object(self, attrs, instance):
        """ change password """
        user = instance.user
        user.set_password(attrs["password1"])
        user.save()
        # mark password reset object as reset
        instance.reset = True
        instance.save()

        return instance


class SportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sport
        fields = ('id', 'name')


class ActivityDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityDetails


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Unit
        fields = ('id', 'name', 'metric', 'imperial')


class TagsSerializer(serializers.Field):

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class ExerciseTypeSerializer(serializers.ModelSerializer):

    synonyms = TagsSerializer()

    class Meta:
        model = models.ExerciseType
        fields = ('id', 'name', 'unit', 'quantity', 'repetition', 'synonyms')


class RepetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Repetition
        fields = ('id', 'unit', 'quantity', 'repetition')


class ExerciseSerializer(serializers.ModelSerializer):

    reps = RepetitionSerializer(many=True, required=False)

    class Meta:
        model = models.Exercise
        fields = ('id', 'type', 'reps')

    # def save_object(self, obj, **kwargs):
    #     post = self.context.get('post', None)
    #     if post is not None:
    #         obj.post = post
    #     return super(ExerciseSerializer, self).save_object(obj, **kwargs)


class PostUserSerializer(serializers.ModelSerializer):

    profile_photo = serializers.ImageField(source='profile.profile_photo')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_photo')


class PostSerializer(serializers.ModelSerializer):

    activity_details = ActivityDetailsSerializer(required=False)
    # exercise = ExerciseSerializer(many=True, read_only=True)
    exercises = ExerciseSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)
    photo = Photo(required=False)

    class Meta:
        model = models.Post
        exclude = ('hidden',)
        read_only_fields = (
            "like_number", "comment_number",
        )

    def save_object(self, obj, **kwargs):
        user = self.context.get('user', None)
        if user is not None:
            obj.user = user
        super(PostSerializer, self).save_object(obj, **kwargs)


class PostLikeSerializer(serializers.ModelSerializer):

    user = PostUserSerializer()

    class Meta:
        model = models.PostLike
        read_only_fields = (
            "created_at",
        )
        exclude = ('post',)


class PostCommentSerializer(serializers.ModelSerializer):

    user = PostUserSerializer()

    class Meta:
        model = models.PostComment
        read_only_fields = (
            "created_at",
        )
        exclude = ('post',)

