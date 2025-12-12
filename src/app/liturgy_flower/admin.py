from django.contrib import admin

from app.liturgy_flower.models import LiturgyFlower


@admin.register(LiturgyFlower)
class LiturgyFlowerAdmin(admin.ModelAdmin):
    pass
