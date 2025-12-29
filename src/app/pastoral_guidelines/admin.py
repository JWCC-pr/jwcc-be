from django.contrib import admin

from app.pastoral_guidelines.models import PastoralGuidelines


@admin.register(PastoralGuidelines)
class PastoralGuidelinesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "subtitle", "created_at"]

    def has_add_permission(self, request):
        """이미 1개가 등록되어 있으면 추가 불가"""
        if PastoralGuidelines.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
