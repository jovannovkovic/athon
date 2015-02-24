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


class AthonUserSerializer(DRFModelSerializer):
    """ Serializer for AthonUser entity which includes django's user entity.

    """
    username = serializers.Field(source='user.username')
    email = serializers.Field(source='user.email')
    gender = IntegerField(required=False)

    class Meta:
        model = models.AthonUser
        read_only_fields = (
            "followers_number", "following_number"
        )
        exclude = ('follow_users',)


class FollowAthonUserSerializer(serializers.ModelSerializer):

    username = serializers.Field(source='user.username')
    first_name = serializers.Field(source='user.first_name')
    last_name = serializers.Field(source='user.last_name')

    class Meta:
        model = models.AthonUser
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
