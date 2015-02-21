from django.db.utils import IntegrityError


class FollowingHimselfError(IntegrityError):
    """ Thrown when user tries to follow himself (which is useless, and
    therefore not allowed).

    """
    pass
