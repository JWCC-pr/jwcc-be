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
    list_display = ["title", "user", "created_at", "hit_count", "comment_count", "like_count"]
    search_fields = ["user__name", "title"]
    search_help_text = "유저 이름, 제목으로 검색하세요."
    raw_id_fields = ["user"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user")
        return queryset

    def has_add_permission(self, request):
        return False
