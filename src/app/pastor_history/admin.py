from django.contrib import admin

from app.pastor_history.models import PastorHistory


@admin.register(PastorHistory)
class PastorHistoryAdmin(admin.ModelAdmin):
    pass
