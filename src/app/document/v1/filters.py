import django_filters

from app.document.models import Document


class DocumentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
