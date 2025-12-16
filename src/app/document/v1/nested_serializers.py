from rest_framework import serializers

from app.document_file.models import DocumentFile


class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = [
            "file",
        ]
        ref_name = "DocumentDocumentFileSerializer"
