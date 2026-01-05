from django.contrib import admin

from app.department_board.models import DepartmentBoard
from app.department_board_image.models import DepartmentBoardImage


class DepartmentBoardImageInline(admin.StackedInline):
    model = DepartmentBoardImage
    extra = 0
    max_num = 20


@admin.register(DepartmentBoard)
class DepartmentBoardAdmin(admin.ModelAdmin):
    inlines = [DepartmentBoardImageInline]
    list_display = ["title", "user", "created_at", "hit_count", "comment_count", "like_count"]
    search_fields = ["user__name", "title"]
    search_help_text = "유저 이름, 제목으로 검색하세요."
    raw_id_fields = ["user"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user")
        return queryset
