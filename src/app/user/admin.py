from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.template import loader
from django.utils import timezone
from import_export import fields, resources, widgets
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from import_export.widgets import ManyToManyWidget

from app.email_log.models import EmailLog
from app.sub_department.models import SubDepartment
from app.user.models import User


class UserResource(resources.ModelResource):
    id = fields.Field(attribute="id", column_name="ID")
    email = fields.Field(attribute="email", column_name="유저네임")
    name = fields.Field(attribute="name", column_name="이름")
    baptismal_name = fields.Field(attribute="baptismal_name", column_name="세례명")
    birth = fields.Field(
        attribute="birth",
        column_name="생년월일",
        widget=widgets.DateWidget(format="%Y-%m-%d"),
    )
    grade = fields.Field(attribute="grade", column_name="등급")
    is_active = fields.Field(attribute="is_active", column_name="가입승인 여부")
    sub_department_set = fields.Field(
        column_name="세부분과",
        attribute="sub_department_set",
        widget=ManyToManyWidget(model="department.SubDepartment", field="name"),
    )
    base_address = fields.Field(attribute="base_address", column_name="기본주소")
    detail_address = fields.Field(attribute="detail_address", column_name="상세주소")
    created_at = fields.Field(
        attribute="created_at",
        column_name="가입일",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M"),
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "baptismal_name",
            "birth",
            "grade",
            "is_active",
            "sub_department_set",
            "base_address",
            "detail_address",
            "created_at",
        )


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
class UserAdmin(ExportActionModelAdmin):
    resource_class = UserResource
    form = UserAdminForm
    formats = [XLSX]
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
    list_filter = ["sub_department_set", "grade", "is_active"]
    search_fields = ["email", "name", "baptismal_name"]
    search_help_text = "이메일, 이름, 세레명으로 검색하세요."
    raw_id_fields = ["sub_department_set"]
    actions = ["approve_users"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("sub_department_set")
        return queryset

    @admin.action(description="선택된 유저 을/를 가입승인합니다.")
    def approve_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated}명의 사용자가 승인되었습니다.")
        now = timezone.localtime()
        for user in queryset:
            subject = "회원가입 승인"
            context = {
                "name": user.name,
                "email": user.email,
                "approval_date": now.strftime("%Y년 %m월 %d일 %H시 %M분"),
                "login_url": f"https://www.{settings.DOMAIN}/login",
            }
            content = loader.render_to_string("user/register_confirm.html", context)
            email_log = EmailLog.objects.create(
                email=user.email,
                title=subject,
                content=content,
            )
            email_log.send()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_repr",
        "action_flag_display",
        "change_message",
    ]
    list_filter = ["action_time", "content_type", "user"]
    search_fields = ["object_repr", "change_message"]
    date_hierarchy = "action_time"
    readonly_fields = [
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    ]

    def action_flag_display(self, obj):
        flags = {1: "추가", 2: "변경", 3: "삭제"}
        return flags.get(obj.action_flag, obj.action_flag)

    action_flag_display.short_description = "작업 유형"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
