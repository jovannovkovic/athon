from rest_framework import permissions


class IsNotAuthenticated(permissions.IsAuthenticated):
    """
    Restrict access only to unauthenticated users.
    """
    def has_permission(self, request, view, obj=None):
        return not (request.user and request.user.is_authenticated())


class IsUserOrAdmin(permissions.BasePermission):
    """ Allows access to User object's calls for the user himself and for
    the administrators.

    """
    def has_object_permission(self, request, view, obj):
        """ Return True if the user from request has the right to manage the
        obj.
        In this case (for this class), obj should be of type User (can
        be concluded from the class name).
        Note that safe method are allowed to all.
        """
        if request.user is not None and \
                request.user.is_authenticated() and \
                obj == request.user:
            # These users have full access for all requests.
            return True

        # else, forbid non safe methods:
        if request.method not in permissions.SAFE_METHODS:
            return False

        # else, allow safe methods, but hide some fields:
        # (Sorry for using this way to hide fields, but the other way would
        # include adding new fields in serializer (with new names), so all
        # frontend code should be changed then.
        # for hidden_field in obj.HIDDEN_FIELDS:
        #     setattr(obj, hidden_field, None)
        # for hidden_field in obj.HIDDEN_USER_FIELDS:
        #     setattr(obj.user, hidden_field, None)
        return True
