from django.contrib import admin

from app.weekly_bulletin_hit.models import WeeklyBulletinHit


@admin.register(WeeklyBulletinHit)
class WeeklyBulletinHitAdmin(admin.ModelAdmin):
    pass
