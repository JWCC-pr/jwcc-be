from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from app.schedule.models import Schedule


class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # 시작시간과 종료시간은 둘 다 입력하거나 둘 다 비워야 함
        if (start_time and not end_time) or (not start_time and end_time):
            raise ValidationError(
                {
                    "start_time": "시작시간과 종료시간은 함께 입력해야 합니다.",
                    "end_time": "시작시간과 종료시간은 함께 입력해야 합니다.",
                }
            )

        # 시작시간이 종료시간보다 늦은 경우
        if start_time and end_time and start_time >= end_time:
            raise ValidationError(
                {
                    "start_time": "시작시간은 종료시간보다 빨라야 합니다.",
                    "end_time": "시작시간은 종료시간보다 빨라야 합니다.",
                }
            )

        return cleaned_data


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = ["id", "title", "scheduled_at", "start_time", "end_time", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
