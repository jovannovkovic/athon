from athon import models

from django.contrib.auth import get_user_model
from drf_toolbox.serializers import ModelSerializer as DRFModelSerializer
from rest_framework.serializers import ModelSerializer

from rest_framework.fields import IntegerField

class _UserSerializer(ModelSerializer):
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
    user = _UserSerializer()
    gender = IntegerField(required=False)

    class Meta:
        model = models.AthonUser
        read_only_fields = (
            "fallowers_number", "fallowing_number"
        )


