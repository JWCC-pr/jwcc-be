from rest_framework import serializers

from app.notice.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "body",
            "created_at",
            "updated_at",
        ]
