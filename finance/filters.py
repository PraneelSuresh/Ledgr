import django_filters
from finance.models import Transaction
import datetime
from django.db.models import Q


class KindFilter(django_filters.FilterSet):
    kind = django_filters.ChoiceFilter(
        empty_label="All Types",
        label=""
    )

    class Meta:
        model = Transaction
        fields = ['kind']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        distinct_kinds = Transaction.objects.values_list('kind', flat=True).distinct()
        self.filters['kind'].extra['choices'] = [(kind, kind.capitalize()) for kind in distinct_kinds if kind]

        for field_name, field in self.form.fields.items():
            field.widget.attrs.update({'class': 'filter-select'})

class TimeFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.form.fields.items():
                field.widget.attrs.update(
                    {
                        'class': 'filter-select'
                    }
                )

    TIME_OPTIONS = [('this_week', 'This Week'), ('this_month', 'This Month')]
    time_filter = django_filters.ChoiceFilter(
        choices = TIME_OPTIONS,
        method = 'filter_by_time',
        label=False,
        empty_label = "All Time"
    )

    class Meta:
        model = Transaction
        fields = []

    def filter_by_time(self, queryset, name, value):
        if value == "this_week":
            return queryset.filter(Q(date__week=datetime.date.today().isocalendar().week) & Q(date__year=datetime.date.today().isocalendar().year))
        elif value == "this_month":
            return queryset.filter(Q(date__month=datetime.date.today().month) & Q(date__year=datetime.date.today().year))
        return queryset

