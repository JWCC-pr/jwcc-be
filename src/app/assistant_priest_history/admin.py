from django.contrib import admin

from app.assistant_priest_history.models import AssistantPriestHistory


@admin.register(AssistantPriestHistory)
class AssistantPriestHistoryAdmin(admin.ModelAdmin):
    pass
