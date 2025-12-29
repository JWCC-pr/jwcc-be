from django.contrib import admin
from django import forms
from app.weekly_bulletin.models import WeeklyBulletin


class WeeklyBulletinAdminForm(forms.ModelForm):
    class Meta:
        model = WeeklyBulletin
        fields = "__all__"

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file.name.lower().endswith(".pdf"):
            raise forms.ValidationError("주보 파일은 PDF만 업로드할 수 잇습니다.")

        return file


@admin.register(WeeklyBulletin)
class WeeklyBulletinAdmin(admin.ModelAdmin):
    form = WeeklyBulletinAdminForm
    list_display = ["id", "title", "hit_count", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
