import django_filters

from app.board_comment.models import BoardComment


class BoardCommentFilter(django_filters.FilterSet):
    parent_id = django_filters.ModelChoiceFilter(label="부모 댓글 ID", queryset=BoardComment.objects.all())
