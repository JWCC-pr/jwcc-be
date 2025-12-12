from django.contrib import admin

from app.pastoral_guidelines.models import PastoralGuidelines


@admin.register(PastoralGuidelines)
class PastoralGuidelinesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "subtitle", "created_at"]
    search_fields = ["title", "subtitle"]
    search_help_text = "제목, 서브 제목으로 검색하세요."

    def has_add_permission(self, request):
        """이미 1개가 등록되어 있으면 추가 불가"""
        if PastoralGuidelines.objects.exists():
            return False
        return super().has_add_permission(request)
