from rest_framework import serializers

from app.document.models import Document
from app.document.v1.nested_serializers import DocumentFileSerializer


class DocumentSerializer(serializers.ModelSerializer):
    file_set = DocumentFileSerializer(label="파일", many=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file_set",
            "created_at",
            "updated_at",
        ]
