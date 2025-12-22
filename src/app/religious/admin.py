from django.contrib import admin

from app.religious.models import Religious


@admin.register(Religious)
class ReligiousAdmin(admin.ModelAdmin):
    pass
