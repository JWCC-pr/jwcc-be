from rest_framework import serializers

from app.document.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "created_at",
            "updated_at",
        ]
