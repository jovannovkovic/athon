from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import FilterSet, MethodFilter


class UserFilter(FilterSet):
    """ Abstract class used for filters like search for all,
        search by winery and search by region which have all field in common.

    """

    search_term = MethodFilter(action="filter_by_params")

    class Meta():
        model = get_user_model()
        fields = ['search_term']

    def filter_by_params(self, qs, value):
        return qs.filter(Q(username__icontains=value) |
                         Q(first_name__icontains=value))
