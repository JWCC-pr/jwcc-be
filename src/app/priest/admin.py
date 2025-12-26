from django.contrib import admin
from app.priest.models import Priest


@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    pass
