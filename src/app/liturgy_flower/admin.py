from django.contrib import admin

from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower_image.models import LiturgyFlowerImage


class LiturgyFlowerImageInline(admin.StackedInline):
    model = LiturgyFlowerImage
    extra = 0
    min_num = 1
    max_num = 5


@admin.register(LiturgyFlower)
class LiturgyFlowerAdmin(admin.ModelAdmin):
    inlines = [LiturgyFlowerImageInline]
    list_display = ["title", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
