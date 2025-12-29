from django.contrib import admin
from app.priest.models import Priest


@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Priest.objects.count() >= 3:
            return False
        return super().has_add_permission(request)
