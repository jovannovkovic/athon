from django.utils.translation import ugettext as _
from django_enumfield import enum


class Gender(enum.Enum):
    """ Enumeration for gender (male, female). """

    MALE = 1
    FEMALE = 2

    labels = {
    MALE: _('Male'),
    FEMALE: _('Female'),
    }


class FollowStatus(enum.Enum):
    """ Enumeration for follow status (follow, following). """

    FOLLOW = 1
    FOLLOWING = 2

    labels = {
    FOLLOW: _('Follow'),
    FOLLOWING: _('Following')
    }


class Unit(enum.Enum):
    """ Enumeration for follow status (follow, following). """

    METRIC = 1
    US = 2

    labels = {
    METRIC: _('Metric'),
    US: _('US')
    }


class ChallengeResponse(enum.Enum):
    """ Enumeration for follow status (follow, following). """

    ACEPTED = 1
    REJECTED = 2
    PENDING = 3

    labels = {
    ACEPTED: _('Acepted'),
    REJECTED: _('Rejected'),
    PENDING: _('Pending')
    }
