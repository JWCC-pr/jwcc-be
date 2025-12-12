from django.contrib import admin

from app.weekly_bulletin.models import WeeklyBulletin


@admin.register(WeeklyBulletin)
class WeeklyBulletinAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
