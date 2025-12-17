from rest_framework import serializers

from app.notice_file.models import NoticeFile


class NoticeFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeFile
        fields = [
            "file",
        ]
        ref_name = "NoticeNoticeFileSerializer"
