from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from app.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(OrderedModelAdmin):
    list_display = ["id", "move_up_down_links", "name"]
    search_fields = ["name"]
    search_help_text = "배너명으로 검색하세요."
