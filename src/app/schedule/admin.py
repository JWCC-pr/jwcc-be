from django.contrib import admin

from app.schedule.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "scheduled_at", "start_time", "end_time", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
