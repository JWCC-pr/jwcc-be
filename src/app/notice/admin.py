from django.contrib import admin

from app.notice.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_fixed", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
