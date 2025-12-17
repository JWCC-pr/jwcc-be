from django.contrib import admin

from app.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
