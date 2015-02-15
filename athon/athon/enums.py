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


class FallowStatus(enum.Enum):
    """ Enumeration for fallow status (fallow, fallowing). """

    FALLOW = 1
    FALLOWING = 2

    labels = {
    FALLOW: _('Fallow'),
    FALLOWING: _('Fallowing')
    }
