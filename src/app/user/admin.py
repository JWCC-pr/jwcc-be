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
    list_display = [
        "id",
        "email",
        "name",
        "baptismal_name",
        "birth",
        "grade",
        "is_active",
        "created_at",
    ]
    list_filter = ["department_set", "grade", "is_active"]
    search_fields = ["email", "name", "baptismal_name"]
    search_help_text = "이메일, 이름, 세레명으로 검색하세요."
    autocomplete_fields = ["department_set"]
    actions = ["approve_users"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("department_set")
        return queryset

    @admin.action(description="선택된 유저 을/를 가입승인합니다.")
    def approve_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated}명의 사용자가 승인되었습니다.")
