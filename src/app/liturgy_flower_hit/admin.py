from django.contrib import admin

from app.liturgy_flower_hit.models import LiturgyFlowerHit


@admin.register(LiturgyFlowerHit)
class LiturgyFlowerHitAdmin(admin.ModelAdmin):
    pass
