from django.contrib import admin

from app.passing_notice_comment.models import PassingNoticeComment


@admin.register(PassingNoticeComment)
class PassingNoticeCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "passing_notice", "user", "body", "is_deleted", "created_at"]
    search_fields = ["user__name", "body"]
    search_help_text = "유저 이름, 내용으로 검색하세요."
    raw_id_fields = ["passing_notice", "user"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("passing_notice", "user")
        return queryset

    def has_add_permission(self, request):
        return False
