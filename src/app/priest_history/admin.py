from django.contrib import admin

from app.priest_history.models import PriestHistory


@admin.register(PriestHistory)
class PriestHistoryAdmin(admin.ModelAdmin):
    pass
