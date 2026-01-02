from django.contrib import admin

from app.weekly_bulletin_editorial.models import (
    WeeklyBulletinEditorialDraft,
    WeeklyBulletinEditorialFinal,
    WeeklyBulletinEditorialTemplate,
    WeeklyBulletinEditorialStateChoices,
)
from app.weekly_bulletin_editorial_file.models import WeeklyBulletinEditorialFile


class WeeklyBulletinEditorialFileInline(admin.TabularInline):
    model = WeeklyBulletinEditorialFile
    extra = 0
    min_num = 1
    max_num = 20


class WeeklyBulletinEditorialAdmin(admin.ModelAdmin):
    inlines = [WeeklyBulletinEditorialFileInline]
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
    exclude = ["state"]

    default_state = None

    def save_model(self, request, obj, form, change):
        if self.default_state is not None:
            obj.state = self.default_state
        super().save_model(request, obj, form, change)


@admin.register(WeeklyBulletinEditorialDraft)
class WeeklyBulletinEditorialDraftAdmin(WeeklyBulletinEditorialAdmin):
    default_state = WeeklyBulletinEditorialStateChoices.DRAFT


@admin.register(WeeklyBulletinEditorialFinal)
class WeeklyBulletinEditorialFinalAdmin(WeeklyBulletinEditorialAdmin):
    default_state = WeeklyBulletinEditorialStateChoices.FINAL


@admin.register(WeeklyBulletinEditorialTemplate)
class WeeklyBulletinEditorialTemplateAdmin(WeeklyBulletinEditorialAdmin):
    default_state = WeeklyBulletinEditorialStateChoices.TEMPLATE
