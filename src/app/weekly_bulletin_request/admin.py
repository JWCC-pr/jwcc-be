from django.contrib import admin

from app.weekly_bulletin_request.models import WeeklyBulletinRequest


@admin.register(WeeklyBulletinRequest)
class WeeklyBulletinRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user")
        return queryset

    def has_add_permission(self, request):
        return False
