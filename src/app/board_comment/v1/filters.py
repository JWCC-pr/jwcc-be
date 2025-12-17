import django_filters

from app.board.models import Board
from app.board_comment.models import BoardComment


class BoardCommentFilter(django_filters.FilterSet):
    parent_id = django_filters.ModelChoiceFilter(label="부모 댓글 ID", queryset=BoardComment.objects.all())

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get("parent_id") is None:
            queryset = queryset.filter(parent__isnull=True)
        return queryset
