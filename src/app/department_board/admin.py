from django.contrib import admin
from django.core.exceptions import ValidationError

from app.department_board.models import DepartmentBoard
from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage


class DepartmentBoardImageInline(admin.StackedInline):
    model = DepartmentBoardImage
    extra = 0
    max_num = 20


class DepartmentBoardFileInline(admin.StackedInline):
    model = DepartmentBoardFile
    extra = 0
    max_num = 20


@admin.register(DepartmentBoard)
class DepartmentBoardAdmin(admin.ModelAdmin):
    inlines = [DepartmentBoardImageInline, DepartmentBoardFileInline]
    list_display = [
        "title",
        "user",
        "department",
        "sub_department",
        "is_pinned",
        "is_secret",
        "created_at",
        "hit_count",
        "comment_count",
        "like_count",
    ]
    search_fields = ["user__name", "title"]
    search_help_text = "유저 이름, 제목으로 검색하세요."
    raw_id_fields = ["user"]
    exclude = ["department"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user", "department", "sub_department")
        return queryset

    def save_model(self, request, obj, form, change):
        obj.department = obj.sub_department.department

        if obj.is_pinned:
            pinned_count = (
                DepartmentBoard.objects.filter(
                    sub_department=obj.sub_department,
                    is_pinned=True,
                )
                .exclude(id=obj.id)
                .count()
            )

            if pinned_count >= 5:
                raise ValidationError("고정글은 최대 5개까지만 등록할 수 있습니다.")

        super().save_model(request, obj, form, change)
