from django.contrib import admin

from app.passing_notice.models import PassingNotice


@admin.register(PassingNotice)
class PassingNoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "district",
        "age",
        "funeral_mass_at",
        "funeral_mass_location",
        "chief_mourner",
        "encoffinment_at",
        "departure_at",
        "created_at",
    ]
    search_fields = ["name", "district"]
    search_help_text = "고인 성함, 소속 구역으로 검색하세요."
