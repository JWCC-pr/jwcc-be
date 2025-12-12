from django.contrib import admin

from app.passing_notice.models import PassingNotice


@admin.register(PassingNotice)
class PassingNoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "baptismal_name",
        "funeral_start_at",
        "funeral_end_at",
        "encoffinment_at",
        "departure_at",
        "created_at",
    ]
    search_fields = ["name", "baptismal_name"]
    search_help_text = "고인 성함, 세례명으로 검색하세요."
