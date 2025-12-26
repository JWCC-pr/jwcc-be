from django.contrib import admin

from app.religious_history.models import ReligiousHistory


@admin.register(ReligiousHistory)
class ReligiousHistoryAdmin(admin.ModelAdmin):
    pass
