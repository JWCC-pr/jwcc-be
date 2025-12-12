from django import forms
from django.contrib import admin

from app.user.models import User


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={"class": "vTextField"}),
        required=False,
        help_text="변경시에만 입력하세요.",
    )

    class Meta:
        model = User
        fields = "__all__"
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["password"].required = True

    def save(self, commit=True):
        password = self.cleaned_data.get("password", None)
        instance = super().save(commit=False)
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ["id", "department", "email", "name", "baptismal_name", "is_accepted", "created_at"]
    list_filter = ["department", "is_accepted"]
    search_fields = ["email", "name", "baptismal_name"]
    search_help_text = "이메일, 이름, 세레명으로 검색하세요."
    autocomplete_fields = ["department"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("department")
        return queryset
