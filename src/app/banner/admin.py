from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from app.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(OrderedModelAdmin):
    list_display = ["id", "move_up_down_links", "name"]
    search_fields = ["name"]
    search_help_text = "배너명으로 검색하세요."

    def delete_model(self, request, obj):
        """단일 배너 삭제 시 최소 1개 유지"""
        total_count = Banner.objects.count()
        if total_count <= 1:
            self.message_user(request, "최소 1개의 배너는 유지되어야 합니다.", level="ERROR")
            return
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """다중 배너 삭제 시 최소 1개 유지"""
        total_count = Banner.objects.count()
        delete_count = queryset.count()

        if total_count - delete_count < 1:
            self.message_user(request, "최소 1개의 배너는 유지되어야 합니다.", level="ERROR")
            return
        super().delete_queryset(request, queryset)
