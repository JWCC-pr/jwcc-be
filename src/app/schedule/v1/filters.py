import django_filters

from app.schedule.models import Schedule


class ScheduleFilter(django_filters.FilterSet):
    year = django_filters.CharFilter(label="연도", field_name="scheduled_at", lookup_expr="year", required=True)
    month = django_filters.CharFilter(label="월", field_name="scheduled_at", lookup_expr="month", required=True)
