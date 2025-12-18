from django.db.models import F
from rest_framework import serializers

from app.passing_notice.models import PassingNotice
from app.passing_notice_comment.models import PassingNoticeComment
from app.passing_notice_comment.v1.nested_serializers import UserSerializer


class PassingNoticeCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)

    class Meta:
        model = PassingNoticeComment
        fields = [
            "id",
            "user",
            "body",
            "is_owned",
            "is_modified",
            "is_deleted",
            "created_at",
        ]
        extra_kwargs = {
            "is_deleted": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        validated_data["passing_notice_id"] = self.context["view"].kwargs["passing_notice_id"]
        validated_data["user_id"] = self.context["request"].user.id
        instance = super().create(validated_data)
        PassingNotice.objects.filter(id=instance.passing_notice_id).update(comment_count=F("comment_count") + 1)
        return instance

    def update(self, instance, validated_data):
        validated_data["is_modified"] = True
        instance = super().update(instance, validated_data)
        return instance
