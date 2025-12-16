from django.contrib import admin

from app.document.models import Document
from app.document_file.models import DocumentFile


class DocumentFileInline(admin.TabularInline):
    model = DocumentFile
    extra = 0
    min_num = 1
    max_num = 5


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    inlines = [DocumentFileInline]
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]
    search_help_text = "제목으로 검색하세요."
