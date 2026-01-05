import django_filters

from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial


class WeeklyBulletinEditorialFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
