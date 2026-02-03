from django.contrib import admin
from django.core.exceptions import ValidationError

from app.department_board.models import DepartmentBoard
from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage
from app.user.models import UserGradeChoices


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
    list_filter = ["department", "sub_department", "is_pinned", "is_secret"]
    search_fields = ["user__name", "title"]
    search_help_text = "유저 이름, 제목으로 검색하세요."
    raw_id_fields = ["user"]
    exclude = ["department"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user", "department", "sub_department")
        return queryset

    def save_model(self, request, obj, form, change):
        allowed_grades = {
            UserGradeChoices.GRADE_01,
            UserGradeChoices.GRADE_02,
            UserGradeChoices.GRADE_03,
            UserGradeChoices.GRADE_04,
        }
        if obj.is_pinned and request.user.grade not in allowed_grades:
            raise ValidationError("공지글 작성 권한이 없습니다.")

        if change and obj.pk:
            original = DepartmentBoard.objects.filter(pk=obj.pk).only("user_id", "is_pinned").first()
            if original and original.is_pinned and not obj.is_pinned:
                if request.user.grade != UserGradeChoices.GRADE_01 and original.user_id != request.user.id:
                    raise ValidationError("자신이 등록한 공지만 해제할 수 있습니다.")
            if original and obj.is_pinned:
                if request.user.grade != UserGradeChoices.GRADE_01 and original.user_id != request.user.id:
                    raise ValidationError("자신이 등록한 공지만 수정할 수 있습니다.")

        obj.department = obj.sub_department.department
        obj.full_clean()
        super().save_model(request, obj, form, change)
