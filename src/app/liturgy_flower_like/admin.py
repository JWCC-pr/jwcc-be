from django.contrib import admin

from app.liturgy_flower_like.models import LiturgyFlowerLike


@admin.register(LiturgyFlowerLike)
class LiturgyFlowerLikeAdmin(admin.ModelAdmin):
    pass
