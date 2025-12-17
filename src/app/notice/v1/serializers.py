from rest_framework import serializers

from app.notice.models import Notice
from app.notice.v1.nested_serializers import NoticeFileSerializer


class NoticeSerializer(serializers.ModelSerializer):
    file_set = NoticeFileSerializer(label="파일", many=True, read_only=True)

    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "body",
            "file_set",
            "created_at",
            "updated_at",
        ]
