import django_filters
from finance.models import Transaction


class KindFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['kind']
