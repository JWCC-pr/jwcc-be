import django_filters

from app.passing_notice_comment.models import PassingNoticeComment


class PassingNoticeCommentFilter(django_filters.FilterSet):
    parent_id = django_filters.ModelChoiceFilter(label="부모 댓글 ID", queryset=PassingNoticeComment.objects.all())
