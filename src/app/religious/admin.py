from django.contrib import admin

from app.religious.models import Religious


@admin.register(Religious)
class ReligiousAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Religious.objects.count() >= 3:
            return False
        return super().has_add_permission(request)
