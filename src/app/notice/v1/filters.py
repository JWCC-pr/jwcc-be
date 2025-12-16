import django_filters

from app.notice.models import Notice


class NoticeFilter(django_filters.FilterSet):
    is_fixed = django_filters.BooleanFilter(label="고정여부")
