from django.contrib import admin

from app.liturgy_flower_comment.models import LiturgyFlowerComment


@admin.register(LiturgyFlowerComment)
class LiturgyFlowerCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "liturgy_flower", "user", "parent", "body", "is_deleted", "created_at"]
    search_fields = ["user__name", "body"]
    search_help_text = "유저 이름, 내용으로 검색하세요."
    raw_id_fields = ["liturgy_flower", "user", "parent"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("liturgy_flower", "user", "parent")
        return queryset

    def has_add_permission(self, request):
        return False
