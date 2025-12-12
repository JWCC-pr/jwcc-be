from django.contrib import admin

from app.board.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "hit_count", "comment_count", "like_count"]
    search_fields = ["user__name", "title"]
    search_help_text = "유저 이름, 제목으로 검색하세요"
    raw_id_fields = ["user"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user")
        return queryset

    def has_add_permission(self, request):
        return False
