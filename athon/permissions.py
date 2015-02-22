from rest_framework import permissions


class IsNotAuthenticated(permissions.IsAuthenticated):
    """
    Restrict access only to unauthenticated users.
    """
    def has_permission(self, request, view, obj=None):
        return not (request.user and request.user.is_authenticated())
