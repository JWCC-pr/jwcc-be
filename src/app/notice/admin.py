from django.contrib import admin

from app.notice.models import Notice
from app.notice_file.models import NoticeFile


class NoticeFileInline(admin.TabularInline):
    model = NoticeFile
    extra = 0
    min_num = 0
    max_num = 5


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    inlines = [NoticeFileInline]
    list_display = ["id", "title", "is_fixed", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
